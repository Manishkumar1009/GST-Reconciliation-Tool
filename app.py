import sys
import os
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ui_main import Ui_MainWindow

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Connect Buttons
        self.ui.btnPurchase.clicked.connect(self.load_purchase)
        self.ui.btnGSTR2A.clicked.connect(self.load_gstr2a)
        self.ui.btnRun.clicked.connect(self.run_reconciliation)
        self.ui.btnOpenFolder.clicked.connect(self.open_output_folder)

        # Variables
        self.purchase_path = ""
        self.gstr2a_path = ""

        # Output directory
        self.output_dir = os.path.join(os.path.expanduser("~"), "Documents", "GST_Reconciliation")
        os.makedirs(self.output_dir, exist_ok=True)

        # Hide loading label initially
        self.ui.lblLoading.hide()

    def load_purchase(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Purchase Register", "", "Excel/CSV Files (*.xlsx *.xls *.csv)")
        if path:
            self.purchase_path = path
            self.ui.txtPurchase.setText(path)

    def load_gstr2a(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select GSTR2A File", "", "Excel/CSV Files (*.xlsx *.xls *.csv)")
        if path:
            self.gstr2a_path = path
            self.ui.txtGSTR2A.setText(path)

    def run_reconciliation(self):
        if not self.purchase_path or not self.gstr2a_path:
            QMessageBox.warning(self, "Error", "Please select both files!")
            return

        self.ui.progressBar.setValue(0)
        self.ui.lblStatus.setText("Processing...")
        self.ui.lblLoading.show()
        QApplication.processEvents()

        try:
            self.reconcile_files()
            QMessageBox.information(self, "Success", "Reconciliation Completed!")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
        finally:
            self.ui.lblLoading.hide()

    def reconcile_files(self):
        # Step 1 – Read Inputs
        if self.purchase_path.endswith(".csv"):
            purchase = pd.read_csv(self.purchase_path)
        else:
            purchase = pd.read_excel(self.purchase_path)

        if self.gstr2a_path.endswith(".csv"):
            gstr2a = pd.read_csv(self.gstr2a_path)
        else:
            gstr2a = pd.read_excel(self.gstr2a_path)

        self.ui.progressBar.setValue(30)
        QApplication.processEvents()

        # Step 2 – Clean GSTIN & Invoice
        purchase["VendorGSTIN"] = purchase["VendorGSTIN"].astype(str).str.strip().str.upper()
        purchase["InvoiceNo"] = purchase["InvoiceNo"].astype(str).str.strip().str.upper()

        gstr2a["GSTIN_Supplier"] = gstr2a["GSTIN_Supplier"].astype(str).str.strip().str.upper()
        gstr2a["InvoiceNo"] = gstr2a["InvoiceNo"].astype(str).str.strip().str.upper()

        self.ui.progressBar.setValue(50)
        QApplication.processEvents()

        # Step 3 – Merge
        reco = purchase.merge(
            gstr2a,
            left_on=["VendorGSTIN", "InvoiceNo"],
            right_on=["GSTIN_Supplier", "InvoiceNo"],
            how="left",
            suffixes=("", "_2A")
        )

        # Step 4 – Flagging
        reco["Match_Flag"] = reco.apply(
            lambda r: "Missing in GSTR2A" if pd.isna(r["TaxableValue_2A"]) else "Matched", axis=1
        )

        # Step 5 – Save Output
        output_path = os.path.join(self.output_dir, "GST_Reconciliation_Output.xlsx")
        reco.to_excel(output_path, index=False)

        self.ui.progressBar.setValue(100)
        self.ui.lblStatus.setText("Completed ✔")
        QApplication.processEvents()

    def open_output_folder(self):
        os.startfile(self.output_dir)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())

# reconcile.py — SAFE + GUARANTEED SAVE VERSION

import pandas as pd
import numpy as np
import traceback

def run(purchase_file, gstr2a_file, output_file, progress_callback=None):
    try:
        # ------------------------
        # Helper: emit progress
        # ------------------------
        def emit(v):
            try:
                if progress_callback:
                    progress_callback(int(v))
            except:
                pass

        emit(5)

        # ------------------------
        # Load files
        # ------------------------
        if purchase_file.lower().endswith(".xlsx"):
            purchase = pd.read_excel(purchase_file)
        else:
            purchase = pd.read_csv(purchase_file)

        emit(15)

        if gstr2a_file.lower().endswith(".xlsx"):
            gstr2a = pd.read_excel(gstr2a_file)
        else:
            gstr2a = pd.read_csv(gstr2a_file)

        emit(25)

        # ------------------------
        # Basic cleaning
        # ------------------------
        purchase.columns = [c.strip() for c in purchase.columns]
        gstr2a.columns = [c.strip() for c in gstr2a.columns]

        for c in ["VendorGSTIN", "InvoiceNo"]:
            if c in purchase.columns:
                purchase[c] = purchase[c].astype(str).str.strip().str.upper()

        for c in ["GSTIN_Supplier", "InvoiceNo"]:
            if c in gstr2a.columns:
                gstr2a[c] = gstr2a[c].astype(str).str.strip().str.upper()

        emit(35)

        # ------------------------
        # Convert numeric
        # ------------------------
        num_cols_purchase = ["TaxableValue", "BillValue", "CGST", "SGST", "IGST"]
        for col in num_cols_purchase:
            if col in purchase.columns:
                purchase[col] = pd.to_numeric(purchase[col], errors="coerce").fillna(0)

        num_cols_gstr2a = ["TaxableValue", "CGST", "SGST", "IGST"]
        for col in num_cols_gstr2a:
            if col in gstr2a.columns:
                gstr2a[col] = pd.to_numeric(gstr2a[col], errors="coerce").fillna(0)

        emit(50)

        # ------------------------
        # Totals
        # ------------------------
        purchase["TotalTax"] = purchase.get("CGST", 0) + purchase.get("SGST", 0) + purchase.get("IGST", 0)
        purchase["TotalValue"] = purchase.get("BillValue", purchase.get("TaxableValue", 0) + purchase["TotalTax"])

        gstr2a["TotalTax"] = gstr2a.get("CGST", 0) + gstr2a.get("SGST", 0) + gstr2a.get("IGST", 0)
        gstr2a["TotalValue"] = gstr2a.get("TaxableValue", 0) + gstr2a["TotalTax"]

        emit(65)

        # ------------------------
        # Perfect merge
        # ------------------------
        merged = purchase.merge(
            gstr2a,
            left_on=["VendorGSTIN", "InvoiceNo"],
            right_on=["GSTIN_Supplier", "InvoiceNo"],
            how="left",
            suffixes=("", "_2A")
        )

        emit(80)

        # ------------------------
        # Match flags + differences
        # ------------------------
        merged["Match_Flag"] = merged["TotalValue_2A"].isna().map({True: "Missing in GSTR2A", False: "Matched"})
        merged["Value_Diff"] = merged["TotalValue"] - merged["TotalValue_2A"]
        merged["Tax_Diff"] = merged["TotalTax"] - merged["TotalTax_2A"]

        # ------------------------
        # Risk logic
        # ------------------------
        def risk(row):
            if row["Match_Flag"] == "Missing in GSTR2A":
                return "High"
            if abs(row["Value_Diff"]) > 100 or abs(row["Tax_Diff"]) > 10:
                return "Medium"
            return "Low"

        merged["Risk"] = merged.apply(risk, axis=1)

        emit(95)

        # ------------------------
        # GUARANTEED SAVE
        # ------------------------
        merged.to_excel(output_file, index=False)

        emit(100)

        return {"status": "ok"}

    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "trace": traceback.format_exc()
        }

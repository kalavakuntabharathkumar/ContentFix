# Power BI starter

1. In ContentFix, export the issue register to `contentfix_audit.xlsx`.
2. In Power BI Desktop choose **Get data → Excel workbook** and select the export.
3. Build cards for total requests, open requests, and resolved requests.
4. Add a clustered column chart with `issue_type` as the axis, count of `id` as values, and `status` as legend.
5. Add a page-level table with `page`, `issue_type`, and `status`; add slicers for issue type and status.

For repeatable reporting, export a CSV from the same register and use **Get data → Text/CSV**.

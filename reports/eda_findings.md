# 📊 Exploratory Data Analysis (EDA) Findings - Indian Housing Market

## Core Insights & Pipeline Considerations

1. **Synthetic Nature of Raw Listing Price vs Size**:
   - Correlation $r \approx 0.02$ between raw listing price and built-up square footage.
   - Mitigated via city-median normalization and winsorization.

2. **Floor Level Recording Discrepancies**:
   - ~47% of rows in uncleaned samples featured `Floor_No > Total_Floors`.
   - Handled by floor capping and anomaly feature indicator.

3. **Macro Regional Growth Rates**:
   - Tier 1: 8.0% - 8.8% annualized capital appreciation.
   - Tier 2: 6.5% - 7.5% annualized capital appreciation.
   - Tier 3: 6.0% baseline growth.

4. **Multi-Factor Investor Decision Rubric**:
   - Properties passing $\ge 4/6$ benchmark rules exhibit optimal capital compounding and downside protection.

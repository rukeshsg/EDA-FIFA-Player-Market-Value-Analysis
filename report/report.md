# 📊 FIFA Player Market Value Analysis (EDA Report)

---

## 1. Introduction

This project performs **Exploratory Data Analysis (EDA)** on FIFA player data to identify the key factors influencing player market value.  
The analysis focuses on uncovering patterns, relationships, and trends using statistical methods and visualization techniques.

---

## 2. Objective

- Identify factors affecting player market value  
- Analyze relationships between player attributes  
- Develop analytical thinking and data exploration skills  
- Support findings with visual evidence  

---

## 3. Dataset Overview

The dataset contains information about football players, including:

- Age  
- Overall Rating  
- Position  
- Performance metrics  
- Market Value (in million euros)  

The dataset is structured and suitable for statistical and visual analysis.

---

## 4. Data Cleaning

The following preprocessing steps were performed:

- Removed duplicate records  
- Handled missing values  
  - Numerical columns → filled using median  
  - Categorical columns → filled with "Unknown"  
- Converted data types where necessary  

These steps ensured data consistency and reliability.

---

## 5. Exploratory Data Analysis

### 5.1 Statistical Summary

Statistical analysis provided insights into:
- Distribution of player age  
- Variation in market value  
- Overall rating spread  

The dataset shows significant variability in player valuation.

---

### 5.2 Distribution Analysis

<p align="center">
  <a href="../images/outliers/market_value_distribution.png">
    <img src="../images/outliers/market_value_distribution.png" width="45%"/>
  </a>

The market value distribution is **right-skewed**, indicating that a small number of players have significantly higher value compared to the majority.

---

### 5.3 Correlation Analysis

<p align="center">
  <img src="../images/correlations/correlation_heatmap.png" width="40%"/>
</p>

The heatmap reveals:

- Strong positive correlation between **overall rating and market value**
- Moderate relationships between performance metrics and value  

This indicates that player skill level is a key determinant of market value.

---

### 5.4 Relationship Analysis

<a href="../images/distributions/rating_vs_value.png">
    <img src="../images/distributions/rating_vs_value.png" width="45%"/>
  </a>
</p>

A clear positive trend is observed:

- Higher-rated players tend to have higher market value  
- This supports the assumption that performance directly impacts valuation  

---

### 5.5 Outlier Analysis

<p align="center">
  <img src="../images/outliers/market_value_outliers.png" width="45%"/>
</p>


Outliers represent:

- Exceptionally high-value players  
- Possible elite performers or anomalies  

These players significantly influence overall distribution.

---

## 6. Hypothesis-Based Analysis

### Hypothesis:
Higher-rated players have higher market value.

### Result:
Supported.

The scatter plot shows a strong positive relationship, confirming that rating plays a major role in determining value.

---

## 7. Multi-Variable Analysis

Market value is influenced by multiple factors:

- Age + Rating  
- Performance + Rating  

This indicates that valuation is not dependent on a single variable but a combination of attributes.

---

## 8. Feature Importance Thinking

Based on analysis:

1. Overall Rating → strongest influence  
2. Performance metrics → moderate influence  
3. Age → indirect influence  

This aligns with real-world player valuation logic.

---

## 9. Key Insights

- Higher-rated players consistently have higher market value  
- Market value distribution is right-skewed  
- Performance metrics strongly influence valuation  
- Age and rating together impact player value  
- A few players dominate the high-value segment  

---

## 10. Conclusion

The analysis demonstrates that player market value is primarily driven by performance indicators such as overall rating and match statistics.  
While age plays a role, performance remains the most significant factor.

This project highlights the importance of combining statistical analysis and visualization to derive meaningful insights from data.

---

## 11. Dashboard Integration

An interactive Streamlit dashboard was developed to:

- Filter players by age and position  
- Visualize relationships dynamically  
- Explore key insights in real time  

This enhances usability and provides a practical application of the analysis.

---

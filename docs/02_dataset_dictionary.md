# 02_dataset_dictionary.md

## Target

* `Attrition_Flag` → churn indicator (e.g., "Existing Customer" vs "Attrited Customer")

---

## Identifiers

* `CLIENTNUM` → unique customer identifier (do NOT use for modeling)

---

## Customer Profile

* `Customer_Age` → age of the customer
* `Gender` → Male / Female
* `Dependent_count` → number of dependents
* `Education_Level` → categorical (may contain "Unknown")
* `Marital_Status` → categorical
* `Income_Category` → income range category

---

## Product / Account

* `Card_Category` → type of credit card
* `Credit_Limit` → total credit limit
* `Total_Revolving_Bal` → current revolving balance
* `Avg_Open_To_Buy` → available credit

---

## Relationship / Tenure

* `Months_on_book` → tenure with the bank
* `Total_Relationship_Count` → number of products held

---

## Behavior (Highly Important for Churn)

* `Months_Inactive_12_mon` → inactivity in last 12 months
* `Contacts_Count_12_mon` → number of contacts with bank

---

## Transactions

* `Total_Trans_Amt` → total transaction amount
* `Total_Trans_Ct` → total transaction count

---

## Change Metrics (Dynamics)

* `Total_Amt_Chng_Q4_Q1` → change in transaction amount
* `Total_Ct_Chng_Q4_Q1` → change in transaction count

---

## Utilization

* `Avg_Utilization_Ratio` → credit usage ratio

---

## ⚠️ Potential Leakage / Derived Variables

These variables are likely derived from models or transformations and should NOT be used for training:

* `Naive_Bayes_Classifier_Attrition_Flag_Card_Category_Contacts_Count_12_mon_Dependent_count_Education_Level_Months_Inactive_12_mon_1`
* `Naive_Bayes_Classifier_Attrition_Flag_Card_Category_Contacts_Count_12_mon_Dependent_count_Education_Level_Months_Inactive_12_mon_2`

👉 These appear to be outputs of a pre-trained model and will cause **data leakage**.

---

## Data Considerations

When working with this dataset, always check:

* Missing values (especially "Unknown" categories)
* Class imbalance in `Attrition_Flag`
* Strong correlations between features
* Feature scaling (for some models)
* Categorical encoding consistency

---

## Modeling Notes

* Behavioral variables are often strong predictors of churn
* Change metrics (`*_Chng_*`) can capture trends
* Avoid using identifiers or derived model outputs
* Be careful with interpretation (correlation ≠ causation)

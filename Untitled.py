#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import jason


# In[2]:


import json

# Assuming your JSON file is named "data.json" and is in the same directory as your Jupyter Notebook
file_path = 'data.json'

# Open the file and load the JSON data
with open(file_path, 'r') as file:
    data = json.load(file)


# In[3]:


data1 = data['data']


# In[4]:


# total revenue

import datetime


class FLAGS:
    GREEN = 1
    AMBER = 2
    RED = 0
    MEDIUM_RISK = 3  # diplay purpose only
    WHITE = 4  # data is missing for this field


# In[5]:


data1.get("financials")


# In[6]:


data1['financials'][0]


# In[7]:


def latest_financial_index(data: dict):
    """
    Determine the index of the latest standalone financial entry in the data.

    This function iterates over the "financials" list in the given data dictionary.
    It returns the index of the first financial entry where the "nature" key is equal to "STANDALONE".
    If no standalone financial entry is found, it returns 0.

    Parameters:
    - data (dict): A dictionary containing a list of financial entries under the "financials" key.

    Returns:
    - int: The index of the latest standalone financial entry or 0 if not found.
    """
    financials = data.get("financials", [])
    for index, financial in enumerate(financials):
        if financial.get("nature") == "STANDALONE":
            return index
    return 0

# Example usage:
latest_index = latest_financial_index(data1)
print(latest_index)


# In[8]:


def total_revenue(data: dict, financial_index):
    """
    Calculate the total revenue from the financial data at the given index.

    This function accesses the "financials" list in the data dictionary at the specified index.
    It then retrieves the net revenue from the "pnl" (Profit and Loss) section under "lineItems".

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for calculation.

    Returns:
    - float: The net revenue value from the financial data.
    """
    financial_entry = data.get("financials", [])[financial_index]
    pnl_section = financial_entry.get("pnl", {})
    line_items = pnl_section.get("lineItems", {})
    net_revenue = line_items.get("net_revenue", 0)
    return net_revenue

# Example usage:
revenue = total_revenue(data1, 0)
print(revenue)


# In[ ]:





# In[9]:


def total_borrowing(data: dict, financial_index):
    """
    Calculate the ratio of total borrowings to total revenue for the financial data at the given index.

    This function sums the long-term and short-term borrowings from the balance sheet ("bs")
    section of the financial data. It then divides this sum by the total revenue, calculated
    by calling the `total_revenue` function.

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for calculation.

    Returns:
    - float: The ratio of total borrowings to total revenue.
    """
    financial_entry = data.get("financials", [])[financial_index]
    balance_sheet = financial_entry.get("bs", {})
    liabilities = balance_sheet.get("liabilities", {})

    long_term_borrowings = liabilities.get("long_term_borrowings", 0)
    short_term_borrowings = liabilities.get("short_term_borrowings", 0)

    total_borrowings = long_term_borrowings + short_term_borrowings

    # Calculate total revenue using the total_revenue function
    total_revenue_value = total_revenue(data, financial_index)

    # Avoid division by zero
    return total_borrowings / total_revenue_value if total_revenue_value != 0 else 0

# Example usage:
borrowing_ratio = total_borrowing(data1, 0)
print(borrowing_ratio)


# In[ ]:





# In[ ]:





# In[10]:


def iscr(data: dict, financial_index):
    """
    Calculate the Interest Service Coverage Ratio (ISCR) from the financial data at the given index.

    This function accesses the "financials" list in the data dictionary at the specified index.
    It then calculates the ISCR by dividing the operating profit by the interest.

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for calculation.

    Returns:
    - float: The calculated ISCR value.
    """
    # Access the relevant financial entry
    financial_entry = data.get("financials")[financial_index]

    # Extract operating profit and interest values
    operating_profit = financial_entry.get("pnl", {}).get("lineItems", {}).get("operating_profit", 0)
    interest = financial_entry.get("pnl", {}).get("lineItems", {}).get("interest", 0)

    # Avoid division by zero
    if interest == 0:
        return 0.0

    # Calculate ISCR
    iscr_value = operating_profit / interest
    return iscr_value


# In[11]:


def iscr_flag(data: dict, financial_index):
    """
    Determine the flag color based on the Interest Service Coverage Ratio (ISCR) value.

    This function calculates the ISCR value by calling the `iscr` function and then assigns a flag color
    based on the ISCR value. If the ISCR value is greater than or equal to 2, it assigns a GREEN flag,
    otherwise, it assigns a RED flag.

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for the ISCR calculation.

    Returns:
    - FLAGS.GREEN or FLAGS.RED: The flag color based on the ISCR value.
    """
    # Call the iscr function to calculate ISCR value
    iscr_value = iscr(data, financial_index)

    # Define the threshold for ISCR
    iscr_threshold = 2.0

    # Assign flag based on ISCR value
    return FLAGS.GREEN if iscr_value >= iscr_threshold else FLAGS.RED

# Example usage:
flag_color = iscr_flag(data1, 0)
print(flag_color)


# In[16]:


# Define flags
#class FLAGS:
    #GREEN = "GREEN"
    #AMBER = "AMBER"

def total_borrowing(data: dict, financial_index):
    # Your total_borrowing function code here

    def borrowing_to_revenue_flag(data: dict, financial_index):
    """
    Determine the flag color based on the ratio of total borrowings to total revenue.

    This function calculates the ratio of total borrowings to total revenue by calling the `total_borrowing`
    function and then assigns a flag color based on the calculated ratio. If the ratio is less than or equal
    to 0.25, it assigns a GREEN flag, otherwise, it assigns an AMBER flag.

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for the ratio calculation.

    Returns:
    - FLAGS.GREEN or FLAGS.AMBER: The flag color based on the borrowing to revenue ratio.
    """
    # Call the total_borrowing function to calculate the borrowing value
    borrowing_value = total_borrowing(data, financial_index)

    # Calculate the borrowing to revenue ratio
    revenue_value = total_revenue(data, financial_index)
    borrowing_to_revenue_ratio = borrowing_value / revenue_value if revenue_value != 0 else 0.0

    # Define the threshold for the ratio
    ratio_threshold = 0.25

    # Assign flag based on the ratio
    return FLAGS.GREEN if borrowing_to_revenue_ratio <= ratio_threshold else FLAGS.AMBER

# Example usage:
flag_color = borrowing_to_revenue_flag(data1, 0)
print(flag_color)


# In[ ]:





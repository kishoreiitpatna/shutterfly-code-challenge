# Customer Lifetime Value Calculator

This repository contains a Python program for calculating the Lifetime Value (LTV) of customers based on event data. The LTV is the projected revenue that a customer will generate during their lifetime.

## Table of Contents

- [Introduction](#introduction)
- [Usage](#usage)
- [Folder Structure](#folder-structure)
- [Sample Input](#sample-input)
- [Output](#output)
- [Running the Code](#running-the-code)
- [License](#license)

## Introduction

Customer Lifetime Value (LTV) is an essential metric for businesses to understand the long-term value of their customers. This program calculates LTV using event data, which includes customer, site visit, image upload, and order events.

## Usage

To use this code to calculate LTV, follow the instructions below:

### Folder Structure

The repository is structured as follows:

- `src/`: Contains the source code for LTV calculation.
- `input/`: Place your input data file (e.g., `input.json`) with events here.
- `output/`: The result of the LTV calculation will be stored in an output file (e.g., `output.txt`) in this directory.
- `sample_input/`: Sample input data files (one for each event type) for visualization.

### Sample Input

You can use the sample input data files in the `sample_input/` directory to visualize the structure of events. Each file represents a different event type (customer, site visit, image upload, order).

### Output

After running the code, the LTV calculation result will be stored in the `output/` directory in a text file (e.g., `output.txt`). The file will include the top X customers with the highest Simple Lifetime Value (LTV).

### Running the Code

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/your-username/customer-lifetime-value.git

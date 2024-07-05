# EMS Network Diagrammer

A tool to create visualizations/mappings of the networks on the Energy Management Systems at Lawrence Berkeley National Laboratory.

#### Work in progress until 8/9/2024

# [DEMO](https://irimpo.github.io/EMS-Network-Diagrammer/)

## Purpose
There are more than 800 controllers at Lawrence Berkeley National Laboratory that relay critical data for maintenance. This project automates the tedious job of creating diagrams of the network, providing a creative and efficient way to display all the controllers and their relationships by using CSV file reports from various building automation systems: WebCTRL, Metasys, Lutron, and more.

![alt text](https://i.imgur.com/umL2hqY.png)

## Prerequisites

Ensure you have the following installed:
- Python 3.x
- Pyvis
- Pandas

## Setup

1. Clone this repository:
    ```bash
    git clone https://github.com/iRimpo/EMS-Network-Diagrammer
    cd EMS-Network-Diagrammer
    ```

2. Install the required Python packages:
    ```bash
    pip install pyvis pandas
    ```

3. Ensure you have CSV files of controllers formatted correctly according to the specific energy management system (see below for details).

## CSV File Formats

Each energy management system has its own CSV format. Below is an example of WebCTRL:

### WebCTRL

Columns:
- Status
- Boot Version
- Driver Version
- Location
- Full Source
- Serial Number
- Vendor Name
- Local Access Disabled
- Downloaded by

CSV content:
```csv
Status,Boot Version,Driver Version,Location,Full Source,Serial Number,Vendor Name,Local Access Disabled,Downloaded by
Operational,1.0,2.3.4,Room 101/Building 1,Source A,123456,VendorX,No,UserA
Out of service,1.2,3.1.4,Room 202/Building 2,Source B,654321,VendorY,Yes,UserB
```

## Automating CSV Formatting

The project includes a script, csv_editor.py, that automatically formats CSV files from WebCTRL, Metasys, Lutron, Wattstopper, and Encelium to be ready for diagramming.

1. Input your CSV file into the script:
```bash
csv_file = 'your_file.csv'
df = pd.read_csv(csv_file)
```
3. Run whatever csv editor function at the bottom:
```bash
webctrl_csv()
```
3. Execute the python file:
```bash
python csv_editor
```

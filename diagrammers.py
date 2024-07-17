import pandas as pd
from building_info import add_building_images
from pyvis.network import Network

# ---------------------------- WebCTRL ----------------------------
def webctrl(csv_file_path, output_file_path, net=None):
    # Read the CSV file
    df = pd.read_csv(csv_file_path)

    # Print column names to debug
    print("Columns in CSV file:", df.columns)

    # Create a Pyvis Network object if not provided
    if net is None:
        net = Network(height='1000px', width='auto', neighborhood_highlight=True, select_menu=True, bgcolor="white", font_color="black")

    # Add the vendor nodes
    vendors = set()
    vendor = df['Vendor Name'].unique()
    for x in vendor:
        if x not in vendors:
            vendors.add(x)
            tooltip = f"<img src='images/vendor.png' width='100' height='100'><br><strong>Vendor:</strong> {x}"
            net.add_node(str(x), label=str(x), color='blue', image='images/vendor.png', shape='image', size=70, tooltip=tooltip)

    # Add nodes and edges based on the CSV file
    buildings = df['Building'].unique()

    for index in buildings:
        # removing to show all connected, can make filter later if needed
        # if index == 'Unknown':
        #     continue  # Skip adding 'Unknown' as a building node
        
        # Add building node
        image = add_building_images(index)
        tooltip = f"<img src={image} width='80%' height='auto'><br><strong>Building:</strong> {index}"
        net.add_node(str(index), label=str(index), color='green', image='images/location.png', shape='circularImage', size=40, tooltip=tooltip)
        
        # Get the unique vendors for this building
        building_vendors = df[df['Building'] == index]['Vendor Name'].unique()
        
        for vendor_name in building_vendors:
            net.add_edge(str(vendor_name), str(index))
        
        # Filter the controllers for this building
        building_controllers = df[df['Building'] == index]
        
        for idx, row in building_controllers.iterrows():
            # Ensure column names match those in your CSV file
            status = row['Status']
            serial_number = row['Serial Number']
            boot_version = row['Boot Version']
            driver_version = row['Driver Version']
            vendor_name = row['Vendor Name']
            location = row['Location']
            vendor = row['Vendor Name']
            
            # Create a unique identifier for each controller; so all nodes appear
            controller_id = f"{serial_number}_{idx}"
            controller_label = f"{serial_number}"
            tooltip = f"<img src='images/controller.png' width='100' height='100'><br><strong> Vendor:</strong> {vendor_name}<br><strong> Serial Number:</strong> {serial_number}<br><strong>Building:</strong> {index}<br><strong>Status:</strong> {status}<br><strong>Boot Version:</strong> {boot_version}<br><strong>Driver Version:</strong> {driver_version}<br><strong>Location:</strong> {location}"
            
            net.add_node(str(controller_id), label=str(controller_label), tooltip=tooltip, color='red', image='images/controller.png', shape='image', title=vendor)
            net.add_edge(str(index), str(controller_id))
    # # Handle 'Unknown' building separately
    # unknown_controllers = df[df['Building'] == 'Unknown']

    # for _, row in unknown_controllers.iterrows():
    #     status = row['Status']
    #     vendor_name = row['Vendor Name']
    #     serial_number = row['Serial Number']
    #     driver_version = row['Driver Version']
    #     controller_label = f"{serial_number}"
    #     tooltip = f"<img src='images/controller.png' width='100' height='100'><br><strong>Vendor:</strong> {vendor_name}<br><strong>Building:</strong> Unknown <br><strong>Status:</strong> {status}<br>"
        
        # existing_edges = [(edge['from'], edge['to']) for edge in net.get_edges()]

        # Check if the vendor is already connected to a building with this controller to remove duplicate edges (removed to show everything)
        # is_already_connected = False
        # for edge in existing_edges:
        #     if edge[0] == vendor_name and edge[1] != controller_label:
        #         is_already_connected = True
        #         break
        
        # if not is_already_connected:
            # net.add_node(str(controller_label), label=str(controller_label), tooltip=tooltip, color='red', image='images/controller.png', shape='image')
            # net.add_edge(str(vendor_name), str(controller_label))

# ---------------------------- Metasys ----------------------------
def metasys(csv_file_path, output_file_path, net=None):
    # Read the CSV file
    df = pd.read_csv(csv_file_path)

    # Print column names to debug
    print("Columns in CSV file:", df.columns)

    # Create a Pyvis Network object if not provided
    if net is None:
        net = Network(height='1000px', width='auto', neighborhood_highlight=True, select_menu=True, bgcolor="white", font_color="black")

    # Add the vendor nodes
    vendors = set()
    vendor = df['Vendor Name'].unique()
    for x in vendor:
        if x not in vendors:
            vendors.add(x)
            tooltip = f"<img src='images/vendor.png' width='100' height='100'><br><strong>Vendor:</strong> {x}"
            net.add_node(str(x), label=str(x), color='blue', image='images/vendor.png', shape='image', size=70, tooltip=tooltip)

    # Add nodes and edges based on the CSV file
    buildings = df['Building'].unique()

    for index in buildings:
        # if index == 'Unknown':
        #     continue  # Skip adding 'Unknown' as a building node
        
        # Add building node
        image = add_building_images(index)
        tooltip = f"<img src={image} width='80%' height='auto'><br><strong>Building:</strong> {index}"
        net.add_node(str(index), label=str(index), color='green', image='images/location.png', shape='circularImage', size=40, tooltip=tooltip)
        
        # Get the unique vendors for this building
        building_vendors = df[df['Building'] == index]['Vendor Name'].unique()
        
        for vendor_name in building_vendors:
            net.add_edge(str(vendor_name), str(index))
        
        # Filter the controllers for this building
        building_controllers = df[df['Building'] == index]
        
        for idx, row in building_controllers.iterrows():
            # Ensure column names match those in your CSV file
            name = row['Item']
            description = row['Description']
            vendor_name = row['Vendor Name']
            
            controller_label = f"{name}"
            controller_id = f"{name}_{idx}"
            tooltip = f"<img src='images/controller.png' width='100' height='100'><br><strong>Vendor:</strong> {vendor_name}<br><strong>Building:</strong> {index}<br><strong>Description:</strong> {description}"
            
            net.add_node(str(controller_id), label=str(controller_label), tooltip=tooltip, color='red', image='images/controller.png', shape='image', title=vendor_name)
            net.add_edge(str(index), str(controller_id))

    # Handle 'Unknown' building separately
    # unknown_controllers = df[df['Building'] == 'Unknown']

    # for _, row in unknown_controllers.iterrows():
    #     vendor_name = row['Vendor Name']
    #     name = row['Item']
    #     description = row['Description']
    #     controller_label = f"{name}"
    #     tooltip = f"<img src='images/controller.png' width='100' height='100'><br><strong>Vendor:</strong> {vendor_name}<br><strong>Building:</strong> {index}<br><strong>Description:</strong> {description}"
        
        # existing_edges = [(edge['from'], edge['to']) for edge in net.get_edges()]

        # Check if the vendor is already connected to a building with this controller to remove duplicate edges (removed to show everything)
        # is_already_connected = False
        # for edge in existing_edges:
        #     if edge[0] == vendor_name and edge[1] != controller_label:
        #         is_already_connected = True
        #         break
        
        # if not is_already_connected:
            # net.add_node(str(controller_label), label=str(controller_label), tooltip=tooltip, color='red', image='images/controller.png', shape='image')
            # net.add_edge(str(vendor_name), str(controller_label))

# ---------------------------- lutron ----------------------------
def lutron(csv_file_path, output_file_path, net=None):
    # Read the CSV file
    df = pd.read_csv(csv_file_path)

    # Print column names to debug
    print("Columns in CSV file:", df.columns)

    # Create a Pyvis Network object if not provided
    if net is None:
        net = Network(height='1000px', width='auto', neighborhood_highlight=True, select_menu=True, bgcolor="white", font_color="black")

    # Add the vendor nodes
    vendors = set()
    vendor = df['Vendor Name'].unique()
    for x in vendor:
        if x not in vendors:
            vendors.add(x)
            tooltip = f"<img src='images/vendor.png' width='100' height='100'><br><strong>Vendor:</strong> {x}"
            net.add_node(str(x), label=str(x), color='blue', image='images/vendor.png', shape='image', size=70, tooltip=tooltip)

    # Add nodes and edges based on the CSV file
    buildings = df['Building'].unique()

    for index in buildings:
        # if index == 'Unknown':
        #     continue  # Skip adding 'Unknown' as a building node
        
        # Add building node
        image = add_building_images(index)
        tooltip = f"<img src={image} width='80%' height='auto'><br><strong>Building:</strong> {index}"
        net.add_node(str(index), label=str(index), color='green', image='images/location.png', shape='circularImage', size=40, tooltip=tooltip)
        
        # Get the unique vendors for this building
        building_vendors = df[df['Building'] == index]['Vendor Name'].unique()
        
        for vendor_name in building_vendors:
            net.add_edge(str(vendor_name), str(index))
        
        # Filter the controllers for this building
        building_controllers = df[df['Building'] == index]
        
        for idx, row in building_controllers.iterrows():
            # Ensure column names match those in your CSV file
            serial_number = row['Serial Number']
            model_number = row['Model Number']
            vendor_name = row['Vendor Name']
            area_name = row['Area Name']
            device_name = row['Device Name']
            device_type = row['Device Type']
            activation_status = row['Activation Status']
            equipment_room = row['Equipment Room']
            panel = row['Panel']
            processor = row['Processor']
            processor_ip = row['Processor IP']
            
            controller_id = f"{serial_number}_{idx}"
            controller_label = f"{serial_number}"
            tooltip = f"<img src='images/controller.png' width='100' height='100'><br><strong>Vendor:</strong> {vendor_name}<br>" \
          f"<strong>Serial Number:</strong> {serial_number}<br>" \
          f"<strong>Model Number:</strong> {model_number}<br>" \
          f"<strong>Area:</strong> {area_name}<br>" \
          f"<strong>Device Name:</strong> {device_name}<br>" \
          f"<strong>Device Type:</strong> {device_type}<br>" \
          f"<strong>Activation Status:</strong> {activation_status}<br>" \
          f"<strong>Equipment Room:</strong> {equipment_room}<br>" \
          f"<strong>Panel:</strong> {panel}<br>" \
          f"<strong>Processor:</strong> {processor}<br>" \
          f"<strong>Processor IP:</strong> {processor_ip}"
            
            net.add_node(str(controller_id), label=str(controller_label), tooltip=tooltip, color='red', image='images/controller.png', shape='image', title=vendor_name)
            net.add_edge(str(index), str(controller_id))

    # Handle 'Unknown' building separately
    # unknown_controllers = df[df['Building'] == 'Unknown']

    # for _, row in unknown_controllers.iterrows():
    #     serial_number = row['Serial Number']
    #     model_number = row['Model Number']
    #     vendor_name = row['Vendor Name']
    #     area_name = row['Area Name']
    #     device_name = row['Device Name']
    #     device_type = row['Device Type']
    #     activation_status = row['Activation Status']
    #     equipment_room = row['Equipment Room']
    #     panel = row['Panel']
    #     processor = row['Processor']
    #     processor_ip = row['Processor IP']
    #     controller_label = f"{serial_number}"
    #     tooltip = f"<img src='images/controller.png' width='100' height='100'><br><strong>Vendor:</strong> {vendor_name}<br>" \
    #       f"<strong>Model Number:</strong> {model_number}<br>" \
    #       f"<strong>Area:</strong> {area_name}<br>" \
    #       f"<strong>Device Name:</strong> {device_name}<br>" \
    #       f"<strong>Device Type:</strong> {device_type}<br>" \
    #       f"<strong>Activation Status:</strong> {activation_status}<br>" \
    #       f"<strong>Equipment Room:</strong> {equipment_room}<br>" \
    #       f"<strong>Panel:</strong> {panel}<br>" \
    #       f"<strong>Processor:</strong> {processor}<br>" \
    #       f"<strong>Processor IP:</strong> {processor_ip}"
        
        # existing_edges = [(edge['from'], edge['to']) for edge in net.get_edges()]

        # Check if the vendor is already connected to a building with this controller to remove duplicate edges (removed to show everything)
        # is_already_connected = False
        # for edge in existing_edges:
        #     if edge[0] == vendor_name and edge[1] != controller_label:
        #         is_already_connected = True
        #         break
        
        # if not is_already_connected:
        # net.add_node(str(controller_label), label=str(controller_label), tooltip=tooltip, color='red', image='images/controller.png', shape='image')
        # net.add_edge(str(vendor_name), str(controller_label))



# ---------------------------- wattstopper ----------------------------


def wattstopper(csv_file_path, output_file_path, net=None):
    # Read the CSV file
    df = pd.read_csv(csv_file_path)

    # Print column names to debug
    print("Columns in CSV file:", df.columns)

    # Create a Pyvis Network object if not provided
    if net is None:
        net = Network(height='1000px', width='auto', neighborhood_highlight=True, select_menu=True, bgcolor="white", font_color="black")

    # Add the vendor nodes
    vendors = set()
    vendor = df['Vendor Name'].unique()
    for x in vendor:
        if x not in vendors:
            vendors.add(x)
            tooltip = f"<img src='images/vendor.png' width='100' height='100'><br><strong>Vendor:</strong> {x}"
            net.add_node(str(x), label=str(x), color='blue', image='images/vendor.png', shape='image', size=70, tooltip=tooltip)

    # Add nodes and edges based on the CSV file
    buildings = df['Building'].unique()

    for index in buildings:
        # if index == 'Unknown':
        #     continue  # Skip adding 'Unknown' as a building node
        
        # Add building node
        image = add_building_images(index)
        tooltip = f"<img src={image} width='80%' height='auto'><br><strong>Building:</strong> {index}"
        net.add_node(str(index), label=str(index), color='green', image='images/location.png', shape='circularImage', size=40, tooltip=tooltip)
        
        # Get the unique vendors for this building
        building_vendors = df[df['Building'] == index]['Vendor Name'].unique()
        
        for vendor_name in building_vendors:
            net.add_edge(str(vendor_name), str(index))
        
        # Filter the controllers for this building
        building_controllers = df[df['Building'] == index]
        
        for idx, row in building_controllers.iterrows():
            # Ensure column names match those in your CSV file
            time = row['Time Captured (UTC)']
            source = row['Source']
            destination = row['Destination']
            protocol = row['Protocol']
            length = row['Length']
            info = row['Info']
            hw_destination = row['HW Destination']
            vendor_name = row['Vendor Name']
            building = row['Building']
            
            controller_id = f"{source}_{idx}"
            controller_label = f"{source}"
            tooltip = f"<img src='images/controller.png' width='100' height='100'><br><strong>Vendor:</strong> {vendor_name}<br>" \
          f"<strong>IP Address:</strong> {source}<br>" \
          f"<strong>Building:</strong> {building}<br>" \
          f"<strong>Protocol:</strong> {protocol}<br>" \
          f"<strong>HW Destination:</strong> {hw_destination}<br>" \
          f"<strong>Info:</strong> {info}<br>" \
          f"<strong>Time Captured (UTC):</strong> {time}<br>"
            
            net.add_node(str(controller_id), label=str(controller_label), tooltip=tooltip, color='red', image='images/controller.png', shape='image', title=vendor_name)
            net.add_edge(str(index), str(controller_id))

    # Handle 'Unknown' building separately
    # unknown_controllers = df[df['Building'] == 'Unknown']

    # for _, row in unknown_controllers.iterrows():
    #     serial_number = row['Serial Number']
    #     model_number = row['Model Number']
    #     vendor_name = row['Vendor Name']
    #     area_name = row['Area Name']
    #     device_name = row['Device Name']
    #     device_type = row['Device Type']
    #     activation_status = row['Activation Status']
    #     equipment_room = row['Equipment Room']
    #     panel = row['Panel']
    #     processor = row['Processor']
    #     processor_ip = row['Processor IP']
    #     controller_label = f"{serial_number}"
    #     tooltip = f"<img src='images/controller.png' width='100' height='100'><br><strong>Vendor:</strong> {vendor_name}<br>" \
    #       f"<strong>Model Number:</strong> {model_number}<br>" \
    #       f"<strong>Area:</strong> {area_name}<br>" \
    #       f"<strong>Device Name:</strong> {device_name}<br>" \
    #       f"<strong>Device Type:</strong> {device_type}<br>" \
    #       f"<strong>Activation Status:</strong> {activation_status}<br>" \
    #       f"<strong>Equipment Room:</strong> {equipment_room}<br>" \
    #       f"<strong>Panel:</strong> {panel}<br>" \
    #       f"<strong>Processor:</strong> {processor}<br>" \
    #       f"<strong>Processor IP:</strong> {processor_ip}"
        
        # existing_edges = [(edge['from'], edge['to']) for edge in net.get_edges()]

        # Check if the vendor is already connected to a building with this controller to remove duplicate edges (removed to show everything)
        # is_already_connected = False
        # for edge in existing_edges:
        #     if edge[0] == vendor_name and edge[1] != controller_label:
        #         is_already_connected = True
        #         break
        
        # if not is_already_connected:
        # net.add_node(str(controller_label), label=str(controller_label), tooltip=tooltip, color='red', image='images/controller.png', shape='image')
        # net.add_edge(str(vendor_name), str(controller_label))


# ---------------------------- encelium ----------------------------


def encelium(csv_file_path, output_file_path, net=None):
    # Read the CSV file
    df = pd.read_csv(csv_file_path)

    # Print column names to debug
    print("Columns in CSV file:", df.columns)

    # Create a Pyvis Network object if not provided
    if net is None:
        net = Network(height='1000px', width='auto', neighborhood_highlight=True, select_menu=True, bgcolor="white", font_color="black")

    # Add the vendor nodes
    vendors = set()
    vendor = df['Vendor Name'].unique()
    for x in vendor:
        if x not in vendors:
            vendors.add(x)
            tooltip = f"<img src='images/vendor.png' width='100' height='100'><br><strong>Vendor:</strong> {x}"
            net.add_node(str(x), label=str(x), color='blue', image='images/vendor.png', shape='image', size=70, tooltip=tooltip)

    # Add nodes and edges based on the CSV file
    buildings = df['Building'].unique()

    for index in buildings:
        # if index == 'Unknown':
        #     continue  # Skip adding 'Unknown' as a building node
        
        # Add building node
        image = add_building_images(index)
        tooltip = f"<img src={image} width='80%' height='auto'><br><strong>Building:</strong> {index}"
        net.add_node(str(index), label=str(index), color='green', image='images/location.png', shape='circularImage', size=40, tooltip=tooltip)
        
        # Get the unique vendors for this building
        building_vendors = df[df['Building'] == index]['Vendor Name'].unique()
        
        for vendor_name in building_vendors:
            net.add_edge(str(vendor_name), str(index))
        
        # Filter the controllers for this building
        building_controllers = df[df['Building'] == index]
        
        for idx, row in building_controllers.iterrows():
            # Ensure column names match those in your CSV file
            floorplan = row['Floorplan']
            address = row['Address']
            bacnet_name = row['BACnet Name']
            bacnet_id = row['BACnet ID']
            note = row['Note']
            building = row['Building']
            vendor_name = row['Vendor Name']
            
            controller_id = f"{address}_{idx}"
            controller_label = f"{address}"
            tooltip = f"<img src='images/controller.png' width='100' height='100'><br><strong>Vendor:</strong> {vendor_name}<br>" \
          f"<strong>Address:</strong> {address}<br>" \
          f"<strong>Building:</strong> {building}<br>" \
          f"<strong>Location:</strong> {floorplan}<br>" \
          f"<strong>BACnet Name:</strong> {bacnet_name}<br>" \
          f"<strong>BACnet ID:</strong> {bacnet_id}<br>" \
          f"<strong>Notes:</strong> {note}<br>"
            
            net.add_node(str(controller_id), label=str(controller_label), tooltip=tooltip, color='red', image='images/controller.png', shape='image', title=vendor_name)
            net.add_edge(str(index), str(controller_id))

    # Handle 'Unknown' building separately
    # unknown_controllers = df[df['Building'] == 'Unknown']

    # for _, row in unknown_controllers.iterrows():
    #     serial_number = row['Serial Number']
    #     model_number = row['Model Number']
    #     vendor_name = row['Vendor Name']
    #     area_name = row['Area Name']
    #     device_name = row['Device Name']
    #     device_type = row['Device Type']
    #     activation_status = row['Activation Status']
    #     equipment_room = row['Equipment Room']
    #     panel = row['Panel']
    #     processor = row['Processor']
    #     processor_ip = row['Processor IP']
    #     controller_label = f"{serial_number}"
    #     tooltip = f"<img src='images/controller.png' width='100' height='100'><br><strong>Vendor:</strong> {vendor_name}<br>" \
    #       f"<strong>Model Number:</strong> {model_number}<br>" \
    #       f"<strong>Area:</strong> {area_name}<br>" \
    #       f"<strong>Device Name:</strong> {device_name}<br>" \
    #       f"<strong>Device Type:</strong> {device_type}<br>" \
    #       f"<strong>Activation Status:</strong> {activation_status}<br>" \
    #       f"<strong>Equipment Room:</strong> {equipment_room}<br>" \
    #       f"<strong>Panel:</strong> {panel}<br>" \
    #       f"<strong>Processor:</strong> {processor}<br>" \
    #       f"<strong>Processor IP:</strong> {processor_ip}"
        
        # existing_edges = [(edge['from'], edge['to']) for edge in net.get_edges()]

        # Check if the vendor is already connected to a building with this controller to remove duplicate edges (removed to show everything)
        # is_already_connected = False
        # for edge in existing_edges:
        #     if edge[0] == vendor_name and edge[1] != controller_label:
        #         is_already_connected = True
        #         break
        
        # if not is_already_connected:
        # net.add_node(str(controller_label), label=str(controller_label), tooltip=tooltip, color='red', image='images/controller.png', shape='image')
        # net.add_edge(str(vendor_name), str(controller_label))
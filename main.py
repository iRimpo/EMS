import pandas as pd
from diagrammers import webctrl, metasys, lutron
from pyvis.network import Network

# Read the CSV file paths
webctrl_data = 'webctrl.csv'
metasys_data = 'metasys.csv'
lutron_data = "lutron.csv"
demo = 'demo.csv'

# Output HTML file path
output_file_path = 'Diagram.html'
demo_path = "index.html"

# Determine the desired initial height and width percentages
initial_height_percent = 70
initial_width_percent = 70

# Create a Pyvis Network object
net = Network(height='500px', width='70%', neighborhood_highlight=True, select_menu=True, bgcolor="white", font_color="black", filter_menu=True, layout=False)

# Call diagrammers to generate network diagrams
# webctrl(demo, demo_path, net=net)
webctrl(webctrl_data, output_file_path, net=net)
metasys(metasys_data, output_file_path, net=net)
lutron(lutron_data, output_file_path, net=net)

# Set physics options
# net.show_buttons(filter_=['physics'])
net.set_options("""
var options = {
  "physics": {
    "enabled": true,
    "forceAtlas2Based": {
      "theta": 1,
      "gravitationalConstant": -50,
      "springLength": 100,
      "avoidOverlap": 0.5
    },
    "minVelocity": 0.75,
    "solver": "forceAtlas2Based",
    "stabilization": {
      "enabled": true,
      "iterations": 1000,
      "updateInterval": 25
    }
  }
}
""")

# JavaScript to stop physics after stabilization
stabilization_js = """
<script type="text/javascript">
    document.addEventListener("DOMContentLoaded", function() {
        var network = window.network;
        network.once('stabilizationIterationsDone', function() {
            network.stopSimulation();
        });
    });
</script>
"""

# Display the network diagram in the HTML file
net.show(output_file_path, notebook=False)

# JavaScript for dynamically setting height and width based on screen size
dynamic_js = """
<script type="text/javascript">
    document.addEventListener("DOMContentLoaded", function() {
        var network = window.network;
        var container = document.getElementById('mynetwork');
        var nodeInfo = document.getElementById('node-info');
        
        // Function to update node information
        function updateNodeInfo(nodeId) {
            var node = network.body.data.nodes.get(nodeId);
            var html = '<h3>Node Information</h3><div>';
            html += node.tooltip || '';  // Use node title as tooltip content
            html += '</div>';
            nodeInfo.innerHTML = html;
            nodeInfo.style.display = 'block';  // Show node info
        }
        
        // Function to reset node information to default message
        function resetNodeInfo() {
            nodeInfo.innerHTML = '<h3>Node Information</h3><div id="info-content">Click on a node to see details here.</div>';
            nodeInfo.style.display = 'block';  // Show node info
        }
        
        // Event listener for network click
        network.on("click", function(params) {
            if (params.nodes.length > 0) {
                var nodeId = params.nodes[0];
                updateNodeInfo(nodeId);
            } else {
                resetNodeInfo();
            }
        });
        
        // Initial resize function
        function resizeNetwork() {
            var windowHeight = window.innerHeight;
            var windowWidth = window.innerWidth;
            var height = Math.floor(windowHeight * %d / 100);
            var width = Math.floor(windowWidth * %d / 100);
            container.style.height = height + 'px';
            container.style.width = width + 'px';
            network.setSize(width + 'px', height + 'px');
        }
        
        // Call resize function on page load
        resizeNetwork();
        
        // Add resize listener
        window.addEventListener('resize', resizeNetwork);
    });
</script>
""" % (initial_height_percent, initial_width_percent)

# Read the generated HTML file and insert the header
with open(output_file_path, 'r') as file:
    html_content = file.read()

# Define the header HTML to insert an image on top of the diagram
header_html = '''
<header style="background-color: #00313C; padding: 10px; text-align: center;">
    <img src="images/berklab.png" alt="Berkeley Lab" style="width: 7%; height: auto; display: block; margin-left: auto; margin-right: auto;">
    <h1 style="margin: 10px 0 0 0; color: white;">Building Automation Systems Diagram</h1>
    <h3 style="margin: 5px 0 10px 0; color: white;">By. Richard Azucenas</h3>
</header>
'''

# Define the container for the Pyvis network and the text box
container_html = '''
<div style="display: flex;">
    <div id="mynetwork"></div>
    <div id="node-info" style="width: 30%; padding: 10px; border-left: 1px solid #ccc; display: block;">
        <h3>Node Information</h3>
        <div id="info-content">Click on a node to see details here.</div>
    </div>
</div>
'''

# Insert the header and container HTML at the beginning of the HTML content
html_content = html_content.replace('<body>', f'<body>\n{header_html}\n{container_html}')
# Insert the dynamic JavaScript and stabilization JavaScript before the closing body tag
html_content = html_content.replace('</body>', dynamic_js + stabilization_js + '</body>')

# Write the modified content back to the HTML file
with open(output_file_path, 'w') as file:
    file.write(html_content)

print(f"Network diagram with header has been saved to {output_file_path}")

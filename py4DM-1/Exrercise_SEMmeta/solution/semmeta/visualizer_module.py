# Written by ahmed khalil ahmed.khalil@areasciencepark.it
#
# Import modules for file system operations (os), JSON parsing (json), 
# and regular expressions -- regex (re)
import os, json, re

# Import PIL for image loading and matplotlib for visualization
from PIL import Image
import matplotlib.pyplot as plt


# Class for visualizing SEM images alongside selected metadata
class SEMVisualizer:
    def __init__(self, json_path, image_path):
        # Store the path to the cleaned metadata JSON file
        self.json_path = json_path
        
        # Store the path to the SEM image file
        self.image_path = image_path
        
        # Define the list of metadata variables to extract and display
        self.variables = [
            "AP_WD",
            "AP_BEAM_TIME",
            "AP_IMAGE_PIXEL_SIZE",
            "AP_HOLDER_HEIGHT",
            "AP_BEAM_CURRENT",
            "AP_HOLDER_DIAMETER"]        
        
        # Initialize an empty dictionary to hold loaded metadata
        self.metadata = {}
        

    # Load metadata from JSON file into self.metadata
    def load_metadata(self):
        with open(self.json_path, 'r') as f:
            self.metadata = json.load(f)


    def clean_value(self, raw_value, variable_name=None):
        """
        Splits a cleaned metadata value into its number and unit.

        The value must be a (signed) number, optionally in scientific
        notation, followed by a unit. Otherwise ("N/A", "N/A") is returned.

        Examples:
            "3.18 mm"         ->  ("3.18", "mm")
            "-13 pA"          ->  ("-13", "pA")
            "2.34e-006 mbar"  ->  ("2.34e-006", "mbar")
            "InLens" or None  ->  ("N/A", "N/A")

        Returns:
            (value, unit) as strings, or ("N/A", "N/A") if no
            number followed by a unit is found
        """

        # Ensure the input is a string before applying regex
        if not isinstance(raw_value, str):
            return ("N/A", "N/A")

        # Use regex to match a signed number (optionally in scientific notation)
        # followed by its unit, e.g. '-13 pA', '2.34e-006 mbar'
        match = re.fullmatch(
            r'([-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?)\s*([^\d\s].*)', raw_value.strip())

        # If a match is found, return the value and the unit
        if match:
            value, unit = match.groups()
            return (value, unit)

        # Return fallback values (Not Available) if no match is found
        return ("N/A", "N/A")


    def extract_variables(self):
        """
        Extracts selected metadata variables and formats
        them into (name, value, unit) tuples for display.
        """
        
        # Initialize list to hold formatted variable rows
        rows = []
        
        # Iterate over each variable of interest
        for var in self.variables:
            # Get raw value from metadata dictionary
            raw = self.metadata.get(var, "N/A")
            
            # Clean and split into value and unit
            value, unit = self.clean_value(raw, variable_name=var)
            
            # Append formatted tuple to the table rows
            rows.append((var, value, unit))
        
        # Return the list of formatted metadata rows
        return rows
        

    def show_image_with_table(self):
        """
        Displays the SEM image alongside a formatted metadata
        table and saves the combined output as a figure.
        """
        
        # Load metadata from JSON into self.metadata
        self.load_metadata()
        
        # Extract and format selected metadata variables
        table_data = self.extract_variables()
        
        # Extract image name (without extension) for output naming
        image_name = os.path.splitext(os.path.basename(self.image_path))[0]

        # Load the SEM image using PIL
        img = Image.open(self.image_path)

        # Create a figure with two vertically stacked subplots
        fig, (ax_img, ax_table) = plt.subplots(2, 1, figsize=(8, 8), gridspec_kw={'height_ratios': [2, 2]})

        # Display the SEM image in grayscale
        ax_img.imshow(img, cmap='gray')
        ax_img.axis('off')
        ax_img.set_title("SEM Image", fontsize=14)

        # Display the metadata table with column headers
        table = ax_table.table(cellText=table_data, colLabels=["Variable", "Value", "Unit"],         
                               loc='center', cellLoc='center')
        
        # Scale the table for better readability
        table.scale(1, 2)
        ax_table.axis('off')
        ax_table.set_title("Extracted Metadata", fontsize=12)

        # Adjust layout to prevent overlap
        plt.tight_layout()
        
        # Ensure output directory exists
        os.makedirs("./output", exist_ok=True)
        
        # Save the figure as a PNG image
        plt.savefig(f"./output/{image_name}.png")
        
        # Display the figure
        plt.show()

# PivotPro

<img src="https://github.com/Limbicnation/PivotPro/blob/main/images/PivotPro3.jpg" alt="PivotPro" width="512" height="512">

PivotPro is a Blender addon designed to enhance your modeling and animation workflow by providing quick access to advanced pivot point controls. 
With PivotPro, you can set the pivot (origin) of your selected object to various strategic points with just a click, organized in an intuitive interface.

## Features

The addon organizes pivot controls into logical groups for easier access:

### Basic
- Center: Set pivot to the center of the object's bounding box

### Axis Extremes
- Min/Max controls for X, Y, and Z axes
- Precisely position pivot at the extremes of your object

### Axis Centers
- Individual X, Y, and Z axis centering
- Centers only the selected axis while maintaining current position on other axes

### Face Centers
- Top/Bottom: Center on XY plane
- Front/Back: Center on XZ plane
- Left/Right: Center on YZ plane

## Installation

1. Download the latest release from the GitHub repository.
2. Open Blender and go to `Edit > Preferences > Add-ons`.
3. Click `Install...` and select the downloaded ZIP file.
4. Enable the addon from the list.

## Usage

1. Select the object in the 3D viewport.
2. Open the PivotPro panel from the sidebar (`View3D > Sidebar > Pivot Set`).
3. Choose from one of the four categories:
   - Use "Basic" for simple center alignment
   - Use "Axis Extremes" to set pivot to the minimum or maximum points
   - Use "Axis Centers" to center along a single axis while maintaining position on others
   - Use "Face Centers" to align with the center of any face

## Tips
- Axis Centers (X, Y, Z) only affect the selected axis, maintaining the current position on other axes
- Face Centers provide quick access to edge and face alignment
- The organized interface helps reduce scrolling and makes frequently used options more accessible

## Version History

### 1.2
- Reorganized UI with logical grouping and visual hierarchy
- Fixed MIN/MAX axis calculations
- Improved Axis Centers functionality
- Enhanced error handling and user feedback
- Added comprehensive tooltips

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

from IPython.html.widgets import ContainerWidget
from IPython.utils.traitlets import CInt

class GridWidget(ContainerWidget):
    """Grid widget
    
    Allows you to easily align widgets to a Bootstrap fluid grid."""
    
    height = CInt(820, help='Pixel height of the entire grid.')
    padding = CInt(10, help='Pixel padding between cells in the grid.')

    def __init__(self, columns, rows, debug=False, **kwargs):
        """Public constructor

        PARAMETERS
        ----------
        columns: int
        rows: int
        debug: bool
            Use rainbow background colors for the cells.
        """
        ContainerWidget.__init__(self)
        # Create the grid
        self.children = self._create_grid(columns, rows, debug=debug)
        # The grid should occupy the entire widget-subarea by default.
        self.set_css('width', '100%')
        # Manually handle height and padding changes.
        self.on_trait_change(self._update_layout, ['height', 'padding'])
        # Update the layout once to set initial values.
        self._update_layout(None, self.height)

    def __getitem__(self, dimensions):
        """Get cell"""
        for dim in dimensions:
            if isinstance(dim, slice):
                raise TypeError('GridWidget does not support slicing')
        if len(dimensions) != 2:
            raise ValueError('GridWidget only supports two dimensions')
        return self.get_cell(*dimensions)

    def get_cell(self, column, row):
        """Get a cell by column and row indicies (0 based)."""
        return self.children[row].children[column]

    def _update_layout(self, name, new):
        """Update the height/padding values of the child widgets.

        Basically this method applies the height and padding traitlet values."""
        rows = len(self.children)
        for row in self.children:
            row.set_css({
                # The height of the cell is a fraction of the total height, 
                # minus all of the padding used vertically between cells.
                'height': str(self.height/rows + (rows-1)*self.padding) + 'px',
                'margin-bottom': str(self.padding) + 'px',
            })
            for cell in row.children:
                cell.set_css({
                    'margin-left': str(self.padding) + 'px',
                })
        
    def _create_cell(self, color=''):
        """Create a grid cell"""
        cell = ContainerWidget()
        cell.set_css({
            'background': color,
            'height': '100%',
            'margin-right': '0px',
            'margin-top': '0px',
            'margin-bottom': '0px',
        })
        return cell

    def _create_grid(self, columns, rows, debug=False):
        """Create the grid rows and cells.

        Returns a list of rows."""
        debug_colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo']
        return [ContainerWidget(children=[self._create_cell(color=debug_colors[min(i*columns+j, len(debug_colors)-1)] if debug else '') for j in range(columns)]) for i in range(rows)]
            
    def _ipython_display_(self, *pargs, **kwargs):
        """Rich display repr for this widget."""
        # Call the normal display logic.
        ContainerWidget._ipython_display_(self, *pargs, **kwargs)
        
        # Call custom add/remove class logic AFTER display.
        for row in self.children:
            row.remove_class('widget-container')
            row.remove_class('vbox')
            row.add_class('row-fluid')
            [c.add_class('span' + str(12/len(row.children))) for c in row.children]

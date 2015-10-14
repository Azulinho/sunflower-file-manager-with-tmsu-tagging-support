import gtk

from plugins.file_list.plugin import Column, FileList
from plugin_base.column_extension import ColumnExtension
from subprocess import check_output


def register_plugin(application):
	"""Register plugin class with application"""
	application.register_column_extension(FileList, TagsColumn)


class BaseColumn(ColumnExtension):
	"""Base class for extending owner and group for item list"""

	def __init__(self, parent, store):
		ColumnExtension.__init__(self, parent, store)
		self._parent = parent
		# create column object
		self._create_column()

	def _create_column(self):
		"""Create column"""
		self._cell_renderer = gtk.CellRendererText()
		self._parent.set_default_font_size(self._get_column_name(), 8)

		self._column = gtk.TreeViewColumn(self._get_column_title())
		self._column.pack_start(self._cell_renderer, True)
		self._column.set_data('name', self._get_column_name())

	def _get_column_name(self):
		"""Returns column name"""
		return None

	def _get_column_title(self):
		"""Returns column title"""
		return None

	def __set_cell_data(self, column, cell, store, selected_iter, data=None):
		"""Set column value"""
		pass


class TagsColumn(BaseColumn):
	"""Adds support for displaying tags in item list"""

	def __set_cell_data(self, column, cell, store, selected_iter, data=None):
		"""Set column value"""
		is_parent = store.get_value(selected_iter, Column.IS_PARENT_DIR)

		value = (store.get_value(selected_iter, Column.TAGS), '')[is_parent]
		cell.set_property('text', value)

	def _create_column(self):
		"""Configure column"""
		BaseColumn._create_column(self)
		self._column.set_cell_data_func(self._cell_renderer, self.__set_cell_data)

	def _get_column_name(self):
		"""Returns column name"""
		return 'tags'

	def _get_column_title(self):
		"""Returns column title"""
		return _('Tags')

	def get_sort_column(self):
		"""Return sort column"""
		return Column.TAGS



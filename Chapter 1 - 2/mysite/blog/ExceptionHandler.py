from django.views.debug import ExceptionReporter

class ExceptionHandler(ExceptionReporter):
	def get_traceback_data(self):

		data = super().get_traceback_data()
		# ... remove/add something here ...
		# for i in data.keys():
		# 	print(i, data[i])
		return data
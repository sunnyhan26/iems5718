$('#date2').DatePicker({
	flat: true,
	date: ['2008-07-31', '2008-07-28'],
	current: '2008-07-31',
	format: 'Y-m-d',
	calendars: 1,
	mode: 'multiple',
	onRender: function(date) {
		return {
			disabled: (date.valueOf() < now.valueOf()),
			className: date.valueOf() == now2.valueOf() ? 'datepickerSpecial' : false
		}
	},
	starts: 0
});


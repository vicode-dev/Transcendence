function parse_code(input, target)
{
	input.value = input.value.replace(/\D/g, '');

	if (input.value.length > 1)
	{
		var next_input = document.getElementById(`int${target}`);
		var i = 1;
		while (next_input && i < input.value.length)
		{
			next_input.value = input.value.charAt(i);
			next_input.focus();
			next_input = document.getElementById(`int${target + i}`);
			i++;
		}
		input.value = input.value.charAt(0);
	}
}
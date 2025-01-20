function delete_account()
{
	
}

async function check_otp_code(event)
{
	const form_id = "otp-form"

	event.preventDefault();

	const form = document.getElementById(form_id)
	const formData = new FormData(form);

	try {
		const response = await fetch(`/api/authentication/otp/validate/`, {
			method: "POST",
			headers: {
				'X-CSRFToken': csrftoken,
			},
			mode: 'same-origin',
			body: formData
			});
	if (response.status == 401 || response.status == 400)
	{
		document.getElementById('enter-code').innerHTML = 
`<input type="text" class="col-sm-9 form-control"
	placeholder="${await response.text()}" name="otp-code" id="otp-code" required>	
`
		return
	}
	} catch (error) {
		// console.error(error);
		document.getElementById('content').innerHTML = "Internal error.";
	}
	await loadPage('/settings/', false)
}

async function disable_otp()
{
	await fetch("/api/authentication/otp/disable/");
	await loadPage('/settings/', false)
}
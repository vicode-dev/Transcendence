function generate_qr_code()
{
	const button = document.getElementById("otp-container");
	if (button)
	{
		const image = `<img src="/api/authentication/otp/qr-code/" alt="otp-qr-code.webp"></img>`
		const form =
`
<form action="/otp/" method="post" class="form-horizontal" id="otp-form">
	<div class="form-group">
		<label for="login" class="control-label">2Af Code</label>
		<div id="enter-code">
		<input
			type="text" class="col-sm-5 form-control"
			placeholder="000 000" name="otp-code" id="otp-code" required>
	</div>

	<div class="form-group"> 
		<button
			type="submit"
			class="col-sm-offset-3 col-sm-5 btn btn-success btn-block"
			onclick="check_otp_code(event);"
		>
		<i class="fa-solid fa-check"></i>
		</button>
	</div>
</form>`
		
		button.innerHTML = `\n\t${image}\n\t${form}\n`;
	}
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
		console.log(response)
	if (response.status == 401 || response.status == 400)
	{
		document.getElementById('enter-code').innerHTML = 
`<input type="text" class="col-sm-9 form-control"
	placeholder="ERROR" name="otp-code" id="otp-code" required>	
`
		return
	}
	} catch (error) {
		console.error(error);
		document.getElementById('content').innerHTML = "Internal error.";
	}
	document.getElementById('otp-container').innerHTML = 
	`<button type="button" id="disable_otp" onclick="disable_otp()" class="btn btn-danger">
	Disable Double Authentication</button>`
}

async function check_otp_state()
{
	const result = await fetch("/api/authentication/otp/enabled/");
	const response = await result.text();
	const otp_container = document.getElementById('otp-container');

	if (!otp_container)
		return ;
	if (response == "True")
		otp_container.innerHTML = 
			`<button type="button" id="disable_otp" onclick="disable_otp()" class="btn btn-danger">
Disable Double Authentication</button>`
	else
		otp_container.innerHTML =
`<button type="button" id="generate_otp" onclick="generate_qr_code()" class="btn btn-danger">
Add Double Authentication</button>`
}

async function disable_otp()
{
	await fetch("/api/authentication/otp/disable/");
	check_otp_state();
}

check_otp_state();
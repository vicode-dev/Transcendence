/**
 * 
 * @param {string} name 
 * @returns {string | undefined}
 */
function getCookie(name)
{
	const nameString = name + "="

	const value = document.cookie.split(";").filter(item => {
		return item.includes(nameString);
	})

	if (value.length)
		return (value[0].substring(nameString.length + 1, value[0].length));
	return (undefined);
}

/**
 * 
 * @param {string} name 
 * @returns {string | undefined}
 */
function deleteCookie(name)
{
	document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC;`;
}

/**
 * 
 * @param {URLSearchParams} params 
 * @return {string}
 */
function getQuery(params)
{
	let query = "?";
	params.forEach(param => {
		if (param != "redirect_url")
		{
			query = `${query}&${encodeURIComponent(param)}`;
		}
	})
	return (query);
}

function checkSession(first = true, wait_for_otp = false)
{
	if (first)
		loadPage("/loading/", false)

	const update = getCookie("update");
	const otp = getCookie("otp");
	if (wait_for_otp && otp == "required")
		setTimeout(checkSession, 3000, false, wait_for_otp)
	else if (update == "session")
	{
		// deleteCookie("update");
		if (otp == "required")
		{
			// if (first)
				loadPage(`/otp/`, false).then();
			return ;
		}
		const	params = new URLSearchParams(window.location.search);
		const	redirect_url = params.get("redirect_url");

		if (redirect_url)
			loadPage(`/${redirect_url}/${getQuery(params)}`).then();
		else
			loadPage(`/home/${getQuery(params)}`).then();
	}
	else // if (session.check)
		setTimeout(checkSession, 3000, false, wait_for_otp)
}


async function fetchForm(event, form_id, update_password = false)
{
	event.preventDefault();

	const form = document.getElementById(form_id)
	const formData = new FormData(form);
	try {
		const response = await fetch(`/${form_id}/`, {
			method: "POST",
			headers: {
				'X-CSRFToken': csrftoken,
			},
			mode: 'same-origin',
			body: formData
			});
		if (response.status == 401 || update_password)
		{
			document.getElementById('content').innerHTML = await response.text();
			return 
		}
	} catch (error) {
		console.error(error);
		document.getElementById('content').innerHTML = "Internal error.";
	}
	if (!update_password)
	{
		// const session = getCookie("session");
		const otp = getCookie("otp");
		// if (session)
		{
			if (otp == "required")
			{
				loadPage(`/otp/`, false).then();
				return ;
			}
			const	params = new URLSearchParams(window.location.search);
			const	redirect_url = params.get("redirect_url");

			if (redirect_url)
				loadPage(`/${redirect_url}/${getQuery(params)}`).then();
			else
				loadPage(`/home/${getQuery(params)}`).then();
		}
	}
}
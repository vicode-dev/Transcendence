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
		return (value[0].substring(nameString.length, value[0].length));
	return (undefined);
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
		console.log(param)
		if (param != "redirect_url")
		{
			query = `${query}&${encodeURIComponent(param)}`;
		}
	})
	return (query);
}

function checkSession(first = true)
{
	
	if (first)
		loadPage("/loading/", false)

	const session = getCookie("session");
	if (session)
	{
		const otp = getCookie("otp");

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
	else
		setTimeout(checkSession, 5000, false)
}


async function fetchForm(event, form_id)
{
	checkSession()
	// console.log("fetch", form_id)
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
		console.log(response)
	if (response.status == 401)
		document.getElementById('content').innerHTML = await response.text();	
	} catch (error) {
		console.error(error);
		document.getElementById('content').innerHTML = "Internal error.";
	}
}

// function listen(element_id)
// {
//     const element = document.getElementById(element_id)

//     if (!element)
//         return ;
// 	element.addEventListener("submit", fetchForm);
// }

// addMain(fec);
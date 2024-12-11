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

function checkSession()
{
	loadPage("/loading/", false)
	const session = getCookie("session");
	if (session)
	{
		const	params = new URLSearchParams(window.location.search);
		const	redirect_url = params.get("redirect_url");

		if (redirect_url)
			loadPage(`/${redirect_url}/${getQuery(params)}`).then();
		else
			loadPage(`/home/${getQuery(params)}`).then();
	}
	else
		setTimeout(checkSession, 3000)
}

document.getElementById("login").addEventListener("submit", async function (event) {
	event.preventDefault();
	const form = event.target;
	const formData = new FormData(form);

	loadPage("/loading/", false);

	try {
	  const response = await fetch("/login/", {
		method: "POST",
		headers: {
            'X-CSRFToken': csrftoken,
        },
        mode: 'same-origin',
		body: formData
	  });
	  console.log(formData)
	  if (!response.ok) {
		throw new Error(`Erreur : ${response.statusText}`);
	  }
  
	//   const result = await response.json();
	//   paper.textContent = `Réponse du serveur : ${result.message}`;
	} catch (error) {
	  console.error(error);
	//   paper.innerHTML = "Une erreur est survenue.";
	}
  });
  
function getQueryParams()
{
	return (new URLSearchParams(location.search));
}
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
function checkSession()
{
	const session = getCookie("session");
	if (session)
	{
		if (window.location.search == '?')
			window.location.replace("https://transcendence.vicode.dev/");
		else
			window.location.replace("https://transcendence.vicode.dev/"+window.location.search);
	}
	else
		setTimeout(checkSession, 3000)
}
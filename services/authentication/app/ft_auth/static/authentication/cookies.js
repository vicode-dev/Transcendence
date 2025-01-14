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
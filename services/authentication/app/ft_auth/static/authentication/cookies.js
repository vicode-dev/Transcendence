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
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
	const	nameString	= name + "="
	let		cookies		= "";

	console.log("i", document.cookie)
	const value = document.cookie.split(";").filter(item => {
		if (!item.includes(nameString))
			cookies=`${item};${cookies}`
	})

	document.cookie = cookies;
	console.log("o", document.cookie)

}
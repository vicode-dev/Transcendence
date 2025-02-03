function copy_token()
{
	if (navigator.clipboard)
	{
		const button = document.getElementById("token");
		if (button)
		{
			const inner = button.innerHTML;
			navigator.clipboard.writeText(inner);
			button.innerHTML = `<i class="fa-solid fa-clipboard-check"></i> ${inner}`;
			setTimeout(() => {
				button.innerHTML = inner
			}, 500);
		}
	}
}

function display_jwt(token)
{
	const button = document.getElementById("token-display");
	if (button)
		button.innerHTML = `<button type="button" id="token" onclick="copy_token()" class="btn btn-light w-100" style="overflow-x: auto; white-space: nowrap; font-size: 0.8rem;">${token}</button>`;
}

async function generate_jwt()
{
	const result = await fetch(`${window.location.origin}/api/authentication/cli/token/?type=persistent`);
	const reply = await result.json();

	if (reply["error"])
	{
		console.error(reply["error"]);
		display_jwt("🥶");
	}
	else
		display_jwt(reply["token"]);
}
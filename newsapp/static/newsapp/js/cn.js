function toggleComment(commentId) {
	htmx.toggleClass(htmx.find(commentId), 'hidden');
	htmx.toggleClass(htmx.find(`${commentId}-toggler`), "after:content-['[-]']");
	htmx.toggleClass(htmx.find(`${commentId}-toggler`), "after:content-['[+]']");
}

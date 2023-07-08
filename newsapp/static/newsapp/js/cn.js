function toggleComment(commentId) {
	htmx.toggleClass(htmx.find(`#comment-${commentId}-children`), 'hidden');
	// htmx.toggleClass(htmx.find(`#comment-${commentId}-children-toggler`), "after:content-['[_-_]']");
	htmx.toggleClass(htmx.find(`#comment-${commentId}-children-toggler`), "after:content-['[_+_]']");
}

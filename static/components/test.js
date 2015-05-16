function render() {
    return (
                React.createElement("div", {className: "commentBox"}, 
                        React.createElement("h1", null, "Comments"), 
                        React.createElement(CommentList, {data: "{{this.props.data}}"}), 
                        React.createElement(CommentForm, null)
                ));
}
CommentBox = React.createClass({react: render});
React.render((
        React.createElement(CommentBox, {data: "{{data}}"})), document.getElementById("content"));
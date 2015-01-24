converter =  new Showdown.converter();
var render = function() {
  
  return (
                        React.createElement("div", {className: "comment"}, 
                                React.createElement("h2", {className: "commentAuthor"}, 
                                      this.props.author
                                ), 
                                converter.makeHtml(this.props.children.toString())
                        ));
}

Comment = React.createClass({ render:render });
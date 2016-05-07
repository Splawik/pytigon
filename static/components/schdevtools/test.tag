<test>
    <h3>{ opts.title }</h3>
    <ul>
            <li each={ item, i in items }>{ item }</li>
    </ul>
    <form onsubmit={ add }>
            <input />
            <button>Add #{ items.length + 1 }</button>
    </form>
    
        <style scoped>
            h3 {
                font-size: 14px;
            }
        </style>
    
    <script>
    
    		this.py_items = list ([]);
    		var add = function (e) {
    			var input = e.target [0];
    			this.py_items.push (input.value);
    			input.value = '';
    		};
    		__pragma__ ('<all>')
    			__all__.add = add;
    		__pragma__ ('</all>')
    	</script>
    
    
</test>
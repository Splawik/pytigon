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
    
    
    
    this.items = [];
    function add(e) {
        var input;
        input = e.target[0];
        this.items.push(input.value);
        input.value = "";
    }
    </script>
    
    
</test>
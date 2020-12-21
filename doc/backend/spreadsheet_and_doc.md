# Generating spreadsheets

There are two possibilities to generate spreadsheets in the Pytigon program.

1. Generating .xlsx files

This method is dedicated to table-based sheets with a lot of data. It allows you to paste a table with data into the template sheet.

## Low level api:

> def transform_xlsx(stream_in, stream_out, transform_list)

parameters:

- steream_in - file with spreadsheet template in xlsx format.
- stream_out - output file in xlsx format.
- transform_list - list with rows in special format.

Row syntax in the list: tranform_list

1. For append row to worksheet use:
   row = [ "ws_name=>", rec[0], recp[2], ... , rec[n] ]
   "ws_name" - name of worksheet in template file.
   row[1:] will be appended to "ws_name" worksheet

2. For append row to default data table or default worksheet:
   row = ["=>", rec[0], recp[2], ... , rec[n] ]
   Syntax similar to the previous one. In this case "ws_name" is empty. Row[1:] will be appended to table named "data_table"
   if this table is defined in template file. Otherwise row[1:] will be appended to worksheet named "data".

3. For change single cell:
   row = ["ws_name//A1", value]  
   The "value" will be written to the cell with the address "A1" located on "ws_name" worksheet.

4. For change single cell alternate syntax:
   row = ["ws_name//A1:value",]

## High level api:

> def render_xlsx(template_name, transform_list)

parameters:

- template_name - name of template file in .xlsx format.
- transform_list - syntax discussed in the previous paragraph

You can use .xlsx tamplates in pytigon generic views.
If in your context there is an element ''doc_type" with the value 'xlsx', the Pytigon system will use the xlsx template instead of standard template.

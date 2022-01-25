<html>
  <head>
    <!--- The stylesheet is symbolically linked from the htdocs as cg-bin folder has execute only --->
    <link type="text/css" rel="stylesheet" href="/cmatrix/static/style.css" />
    <title>Competence Matrix</title>
  </head>
  <body>
    <div>
      <button class="unselbtn" onclick="window.location.href='cmatrix.py'">Competence matrix</button>
      <button class="unselbtn" onclick="window.location.href='competence.py'">Category competence</button>
      <button class="unselbtn" onclick="window.location.href='pers_cmatrix.py'">Personal competence matrix</button>
      <button class="selbtn" onclick="window.location.href='add_competence.py'">Add competence</button>
      User: {{username}}
    </div>
    <hr>
    <br>
    <form action="update.py?page=add_competence" method="post">
        <table>
            <tr>
        <td class="dropdown">
            <button type=button class="dropbtn" onclick="toggleDropdown()">Competence</button>
            <input type="text" placeholder="Competence.." id="mycompetence" name="mycompetence" onkeyup="filterFunction()" onclick="showDropdown()">
            <div id="myDropdown" class="dropdown-content" onclick="toggleDropdown()">
                % for row in rowcompetence:
                <div id="{{row['id']}}" onclick="getValue(this)">{{row['name']}}</div> 
                % end
            </div>
        </td>
        <td>&nbsp;&nbsp;&nbsp;</td>
        <td>
            <b>Degree of competence</b><br>
            <select name="scale_id">
                % for row in rowscale:
                %   if row['id']!=0:
                      <option value="{{row['id']}}">{{row['name']}}</option>
                %     end
                % end
            </select>
            <br><br><br>
            <b>Category</b><br>
            <select id="category_id" name="category_id">
                % for row in rowcategory:
                    <option value="{{row['id']}}">{{row['name']}}</option>
                % end
            </select>
            <br><br><br>
        <input  class="selbtn" value="Add competence" type="submit" />
        </td></tr>
    </form>
    <script>
        function showDropdown() {
            document.getElementById("myDropdown").classList.remove("show");
            toggleDropdown();
            }

        function toggleDropdown() {
            document.getElementById("myDropdown").classList.toggle("show");
            }

        function filterFunction() {
            var input, filter, a, i;

            input = document.getElementById("mycompetence");
            filter = input.value.toUpperCase();
            div = document.getElementById("myDropdown");
            divlist = div.getElementsByTagName("div");
            for (i = 0; i < divlist.length; i++) {
                txtValue = divlist[i].textContent || divlist[i].innerText;
                if (txtValue.toUpperCase().indexOf(filter) > -1) {
                    divlist[i].style.display = "";
                    }
                else {
                    divlist[i].style.display = "none";
                    }
                }
            document.getElementById("category_id").disabled=false;
            }

        function getText(obj) {
            return obj.textContent || obj.innerText;
            }

        function getValue(obj) {
            document.getElementById("mycompetence").value=getText(obj);
            filterFunction();
            document.getElementById("category_id").disabled=true;
            }
    </script>
  </body>
</html>

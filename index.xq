declare default element namespace "http://cefn.com/org";
let $items := .//text()[parent::c/parent::c/text()[contains(string(.),'Vehicles')]]
return 
<html xmlns="http://www.w3.org/1999/xhtml">
    <body>
       {for $item in $items return string($item)}
    </body>
</html>
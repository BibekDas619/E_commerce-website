    var id_buynow
    if (localStorage.getItem('cart') == null) {
      var cart = {};
    }
    else {
      cart = JSON.parse(localStorage.getItem('cart'));
    }
    var select_value = "";
    function change() {
      var selIndex = document.getElementById("select").selectedIndex;
      var selValue = document.getElementById("select").options[selIndex].innerHTML;
      select_value = selValue;
    }

    function buynow(id) {
      if (select_value == "") {
        console.log("Please select your quantity before moving forward");
      }
      else {
        document.getElementById(id).href = "/checkout_buynow" + "/" + id + "/" + select_value
      }
    }

    function item(id) {
      let idstr = id.toString();
      if (select_value == "") {
        console.log('Please select your quantity before moving forward');
      }
      else if (cart[idstr] != undefined) {
        cart[idstr] = cart[idstr] + parseInt(select_value);
      }
      else {
        cart[idstr] = parseInt(select_value);
      }
      console.log(cart)
      localStorage.setItem('cart', JSON.stringify(cart));
      var items = JSON.parse(localStorage.getItem('cart'));
      var total = Object.values(items).reduce(function (a, b) { return (a + b) })
      document.getElementById('val').innerHTML = parseInt(total);
      location.reload()
    }
    $(document).ready(function () {
      var items = JSON.parse(localStorage.getItem('cart'));
      var keys_str = JSON.stringify(items);
      $("#cart").attr('href', "/cart/" + keys_str)
      $("#frm").attr("action", "bill/" + keys_str)
      $("#final").attr("action", "/" + "order" + "/" + keys_str)

      var total = Object.values(items).reduce(function (a, b) { return (a + b) });
      document.getElementById('val').innerHTML = parseInt(total);
    })


    function del_item(id) {
      console.log($(id).parent("div").attr('id'))
      var r = JSON.parse(localStorage.getItem('cart'))
      delete r[id]
      var m = JSON.stringify(r)
      localStorage.setItem('cart', m)
      location.reload()

    }

    function chg2() {
      var ind = document.getElementById('country').selectedIndex
      var val = document.getElementById('country').options[ind].value
      document.getElementById("hidecountry").value = val
    }

    function chg() {
      var ind = document.getElementById('payment').selectedIndex
      var val = document.getElementById('payment').options[ind].value
      document.getElementById("hidepayment").value = val
      if (val === "card") {
        document.getElementById('card_details').disabled = false
      }
      else {
        document.getElementById('card_details').disabled = true
      }
    }


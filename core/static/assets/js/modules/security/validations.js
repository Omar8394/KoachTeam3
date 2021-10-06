 function getEmail() {
            let emails = {
                "emailPrincipal": document.getElementById("email_pri").value
            };
            document.getElementById("correos").value= JSON.stringify(emails);
            document.getElementById("email_user").value=emails.emailPrincipal;
            return true;
        }
    function getPasswordValidation(){
            let pass1 =document.getElementById("password").value;
            let pass2 =document.getElementById("password2").value;
            if(pass1!==pass2){
                swal("Error","the password and the confirmation password must be the same","error");
                return false;
            }
            return true;
        }
        function getPhone() {
            let telefono=document.getElementById("telefonos_pri");
            let tipo_telefono = document.getElementById("cb_tipo_telefono");
            if(telefono!==null && tipo_telefono!==null) {
                let telefonos = {
                    "telefonoPrincipal": telefono.value,
                    "tipoTPrincipal": tipo_telefono.options[tipo_telefono.selectedIndex].value
                };
                document.getElementById("telefonos").value = JSON.stringify(telefonos);
            }
             return true;
        }



<?php
$target_dir = "uploads/daph/";
$target_file = $target_dir . basename($_FILES["daphfilename"]["name"]);
$fileType = pathinfo($target_file,PATHINFO_EXTENSION);

if (move_uploaded_file($_FILES["daphfilename"]["tmp_name"], $target_file)) {
        echo "The file ". basename( $_FILES["daphfilename"]["name"]). " has been uploaded.";
    } else {
        echo "Sorry, there was an error uploading your file.";
    }
?>
<?php
include_once 'config/database.php';
include_once 'includes/header.php';

if ($_POST) {
    $database = new Database();
    $db = $database->getConnection();
    
    $name = $_POST['name'];
    $email = $_POST['email'];
    $phone = $_POST['phone'];
    $company = $_POST['company'];
    $source = $_POST['source'];
    
    $query = "INSERT INTO leads (name, email, phone, company, source) VALUES (?, ?, ?, ?, ?)";
    $stmt = $db->prepare($query);
    
    if ($stmt->execute([$name, $email, $phone, $company, $source])) {
        echo '<div class="alert alert-success">Lead added successfully!</div>';
    } else {
        echo '<div class="alert alert-danger">Unable to add lead.</div>';
    }
}
?>

<div class="row">
    <div class="col-md-8 mx-auto">
        <div class="card">
            <div class="card-header">
                <h3>📥 Capture New Lead</h3>
            </div>
            <div class="card-body">
                <form action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>" method="post">
                    <div class="row">
                        <div class="col-md-6">
                            <div class="mb-3">
                                <label class="form-label">Full Name *</label>
                                <input type="text" class="form-control" name="name" required>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="mb-3">
                                <label class="form-label">Email *</label>
                                <input type="email" class="form-control" name="email" required>
                            </div>
                        </div>
                    </div>
                    
                    <div class="row">
                        <div class="col-md-6">
                            <div class="mb-3">
                                <label class="form-label">Phone</label>
                                <input type="tel" class="form-control" name="phone">
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="mb-3">
                                <label class="form-label">Company</label>
                                <input type="text" class="form-control" name="company">
                            </div>
                        </div>
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">Lead Source</label>
                        <select class="form-select" name="source">
                            <option value="Website">Website</option>
                            <option value="Referral">Referral</option>
                            <option value="Social Media">Social Media</option>
                            <option value="Email Campaign">Email Campaign</option>
                            <option value="Event">Event</option>
                        </select>
                    </div>
                    
                    <button type="submit" class="btn btn-primary">Add Lead</button>
                </form>
            </div>
        </div>
    </div>
</div>

<?php include_once 'includes/footer.php'; ?>

<?php
include_once 'config/database.php';
include_once 'includes/header.php';

$database = new Database();
$db = $database->getConnection();

$query = "SELECT * FROM leads ORDER BY created_at DESC";
$stmt = $db->prepare($query);
$stmt->execute();
$leads = $stmt->fetchAll(PDO::FETCH_ASSOC);
?>

<div class="d-flex justify-content-between align-items-center mb-4">
    <h2>📋 All Leads</h2>
    <a href="index.php" class="btn btn-primary">Add New Lead</a>
</div>

<div class="card">
    <div class="card-body">
        <?php if (count($leads) > 0): ?>
            <div class="table-responsive">
                <table class="table table-striped table-hover">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Phone</th>
                            <th>Company</th>
                            <th>Source</th>
                            <th>Status</th>
                            <th>Created</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($leads as $lead): ?>
                        <tr>
                            <td><?php echo htmlspecialchars($lead['name']); ?></td>
                            <td><?php echo htmlspecialchars($lead['email']); ?></td>
                            <td><?php echo htmlspecialchars($lead['phone']); ?></td>
                            <td><?php echo htmlspecialchars($lead['company']); ?></td>
                            <td>
                                <span class="badge bg-secondary"><?php echo htmlspecialchars($lead['source']); ?></span>
                            </td>
                            <td>
                                <span class="badge bg-<?php 
                                    switch($lead['status']) {
                                        case 'New': echo 'warning'; break;
                                        case 'Contacted': echo 'info'; break;
                                        case 'Qualified': echo 'success'; break;
                                        case 'Lost': echo 'danger'; break;
                                        default: echo 'secondary';
                                    }
                                ?>"><?php echo htmlspecialchars($lead['status']); ?></span>
                            </td>
                            <td><?php echo date('M j, Y', strtotime($lead['created_at'])); ?></td>
                        </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>
        <?php else: ?>
            <div class="text-center py-4">
                <p class="text-muted">No leads found. <a href="index.php">Add your first lead!</a></p>
            </div>
        <?php endif; ?>
    </div>
</div>

<?php include_once 'includes/footer.php'; ?>

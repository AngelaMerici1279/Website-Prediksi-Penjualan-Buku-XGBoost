<!-- Sidebar -->
<ul class="navbar-nav sidebar sidebar-dark accordion" id="accordionSidebar" style="background: linear-gradient(180deg, #ff9900, #ff6600);">
    <a class="sidebar-brand d-flex align-items-center justify-content-center" href="<?= base_url('dashboard/dashboardp'); ?>">
        <div class="sidebar-brand-icon">
            <i class="fa-solid fa-users"></i>
        </div>
        <div class="sidebar-brand-text mx-3">Penjualan</div>
    </a>
    <hr class="sidebar-divider my-0">

    <li class="nav-item">
        <a class="nav-link" href="<?= base_url('dashboard/Penjualan'); ?>">
            <i class="fa-solid fa-chart-simple"></i>
            <span>Dashboard Penjualan</span></a>
    </li>

    <hr class="sidebar-divider">

    <li class="nav-item active">
        <a class="nav-link" href="#" data-toggle="collapse" data-target="#collapsePages" aria-expanded="true"
            aria-controls="collapsePages">
            <i class="fas fa-fw fa-folder"></i>
            <span>Prediksi Penjualan</span>
        </a>
        <div id="collapsePages" class="collapse show" aria-labelledby="headingPages"
            data-parent="#accordionSidebar">
            <div class="bg-white py-2 collapse-inner rounded">
                <h6 class="collapse-header">menu:</h6>
                <a class="collapse-item" href="<?= base_url('penjualan/prediksiPenjualan'); ?>">Prediksi Penjualan Tahun <br>Depan</a>
            </div>
        </div>
    </li>

    <hr class="sidebar-divider">
    <!-- Sidebar Toggler (Sidebar) -->
    <div class="text-center d-none d-md-inline">
        <button class="rounded-circle border-0" id="sidebarToggle"></button>
    </div>

</ul>
<!-- End of Sidebar -->
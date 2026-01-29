<ul class="navbar-nav bg-gradient-primary sidebar sidebar-dark accordion" id="accordionSidebar">
    <a class="sidebar-brand d-flex align-items-center justify-content-center" href="<?= base_url('dashboard/dashboardk'); ?>">
        <div class="sidebar-brand-icon">
            <i class="fa-solid fa-users"></i>
        </div>
        <div class="sidebar-brand-text mx-3">Kepegawaian</div>
    </a>

    <hr class="sidebar-divider my-0">

    <?php $uri = $this->uri->segment(1); ?>

    <li class="nav-item <?= ($uri == 'dashboard/Kepegawaian') ? 'active' : ''; ?>">
        <a class="nav-link" href="<?= base_url('dashboard/kepegawaian'); ?>">
            <i class="fas fa-fw fa-tachometer-alt"></i>
            <span>Dashboard</span></a>
    </li>

    <hr class="sidebar-divider">

    <?php
    $is_pegawai_menu = ($uri == 'data' || $uri == 'pegawai');
    ?>

    <li class="nav-item <?= $is_pegawai_menu ? 'active' : ''; ?>">
        <a class="nav-link <?= $is_pegawai_menu ? '' : 'collapsed'; ?>" href="#" data-toggle="collapse" data-target="#collapsePages" aria-expanded="<?= $is_pegawai_menu ? 'true' : 'false'; ?>"
            aria-controls="collapsePages">
            <i class="fas fa-fw fa-folder"></i>
            <span>Kelola Data Pegawai</span>
        </a>

        <div id="collapsePages" class="collapse <?= $is_pegawai_menu ? 'show' : ''; ?>" aria-labelledby="headingPages"
            data-parent="#accordionSidebar">
            <div class="bg-white py-2 collapse-inner rounded">
                <h6 class="collapse-header">menu:</h6>

                <a class="collapse-item <?= ($uri == 'data') ? 'active' : ''; ?>" href="<?= base_url('data'); ?>">Edit Data Pegawai</a>
                <a class="collapse-item <?= ($this->uri->segment(2) == 'tambahdataPegawai') ? 'active' : ''; ?>" href="<?= base_url('pegawai/tambahdataPegawai'); ?>">Tambah Data Pegawai</a>
            </div>
        </div>
    </li>

    <hr class="sidebar-divider">

    <div class="text-center d-none d-md-inline">
        <button class="rounded-circle border-0" id="sidebarToggle"></button>
    </div>

</ul>
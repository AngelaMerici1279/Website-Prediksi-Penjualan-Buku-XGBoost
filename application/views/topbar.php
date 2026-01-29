<div id="content-wrapper" class="d-flex flex-column">
    <div id="content">
        <nav class="navbar navbar-expand navbar-light bg-white topbar mb-4 static-top shadow">
            <div class="navbar-brand d-flex align-items-center ml-3">
                <img src="<?= base_url('assets/img/kanisius.png'); ?>" 
                     alt="Logo Kanisius" 
                     style="height: 40px; width: auto;">
            </div>
            <ul class="navbar-nav ml-auto">
                <li class="nav-item dropdown no-arrow">
                    <a class="nav-link dropdown-toggle d-flex align-items-center" href="#" id="userDropdown"
                        role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">

                        <!-- FOTO PROFIL -->
                        <img class="img-profile rounded-circle mr-2"
                            src="<?= base_url('assets/img/profile/default.jpg'); ?>"
                            style="width: 32px; height: 32px; object-fit: cover;">

                        <!-- NAMA USER -->
                        <span class="d-none d-lg-inline text-gray-600 small">
                            <?= $this->session->userdata('nama'); ?>
                        </span>
                    </a>

                    <!-- DROPDOWN -->
                    <div class="dropdown-menu dropdown-menu-right shadow animated--grow-in"
                        aria-labelledby="userDropdown">

                        <!-- <a class="dropdown-item" href="<?= base_url('user/profile'); ?>">
                            <i class="fas fa-user fa-sm fa-fw mr-2 text-gray-400"></i>
                            Data Diri
                        </a> -->

                        <div class="dropdown-divider"></div>

                        <a class="dropdown-item" href="<?= base_url('auth/logout'); ?>">
                            <i class="fas fa-sign-out-alt fa-sm fa-fw mr-2 text-gray-400"></i>
                            Logout
                        </a>
                    </div>
                </li>

            </ul>
        </nav>
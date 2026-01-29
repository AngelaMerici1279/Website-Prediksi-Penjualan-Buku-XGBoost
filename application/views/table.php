<?php
$this->load->view('headerdashboard/headerKepegawaian');
$this->load->view('sidebar');
$this->load->view('topbar');

?>

<body id="page-top">

    <!-- Page Wrapper -->
    <div id="wrapper">
        <!-- Content Wrapper -->
        <div id="content-wrapper" class="d-flex flex-column">

            <!-- Main Content -->
            <div id="content">
                <!-- Begin Page Content -->
                <div class="container-fluid">

                    <!-- Page Heading -->
                    <h1 class="h3 mb-2 text-gray-800">Data Pegawai </h1>
                    <?php if ($this->session->flashdata('success')): ?>
                        <div class="alert alert-success alert-dismissible fade show" role="alert" id="success-alert">
                            <?= $this->session->flashdata('success'); ?>
                        </div>

                        <script>
                            // Script untuk menghilangkan popup otomatis setelah 5 detik
                            setTimeout(function() {
                                let alert = document.getElementById('success-alert');
                                if (alert) {
                                    alert.classList.remove('show');
                                    alert.classList.add('fade');
                                    setTimeout(() => alert.remove(), 500); // hapus elemen dari DOM setelah fade out
                                }
                            }, 5000); // 5000 ms = 5 detik
                        </script>
                    <?php endif; ?>

                    <div class="card mb-4">
                        <div class="card-body">
                            <form class="form-inline" method="GET" action="<?= base_url('data'); ?>">
                                <div class="form-group mb-2 mr-3">
                                    <label for="nama" class="mr-2">Nama Pegawai</label>
                                    <input type="text" class="form-control" id="nama" name="nama"
                                        placeholder="Masukkan nama pegawai"
                                        value="<?= $this->input->get('nama'); ?>">
                                </div>

                                <div class="form-group mb-2 mr-3">
                                    <label for="divisi" class="mr-2">Divisi</label>
                                    <select class="form-control" id="divisi" name="divisi">
                                        <option value="">-- Semua Divisi --</option>
                                        <?php foreach ($divisi as $d): ?>
                                            <option value="<?= $d->role; ?>"
                                                <?= ($this->input->get('divisi') == $d->role) ? 'selected' : ''; ?>>
                                                <?= $d->role; ?>
                                            </option>
                                        <?php endforeach; ?>
                                    </select>
                                </div>

                                <button type="submit" class="btn btn-primary mb-2">Cari</button>
                                <a href="<?= base_url('data'); ?>" class="btn btn-secondary mb-2 ml-2">Reset</a>
                            </form>
                        </div>
                    </div>
                    <!-- DataTales Example -->
                    <div class="card shadow mb-4">
                        <div class="card-header py-3">
                            <h6 class="m-0 font-weight-bold text-primary">DataTables Example</h6>
                        </div>
                        <div class="card-body">
                            <div class="table-responsive">

                                <table class="table table-bordered" id="dataTable" width="100%" cellspacing="0">
                                    <thead>
                                        <tr>
                                            <th>id_pegawai</th>
                                            <th>NIK KTP/No. SIM</th>
                                            <th>Nama lengkap</th>
                                            <th>Username</th>
                                            <th>Jenis Kelamin</th>
                                            <th>Email</th>
                                            <th>Divisi</th>
                                            <th>Tanggal Masuk</th>
                                            <th>Status</th>
                                            <th>Gaji</th>
                                            <th>Aksi</th>
                                        </tr>
                                    </thead>
                                    <tfoot>
                                        <tr>
                                            <th>id_pegawai</th>
                                            <th>NIK KTP/No. SIM</th>
                                            <th>Nama lengkap</th>
                                            <th>Username</th>
                                            <th>Jenis Kelamin</th>
                                            <th>Email</th>
                                            <th>Divisi</th>
                                            <th>Tanggal Masuk</th>
                                            <th>Status</th>
                                            <th>Gaji</th>
                                            <th>Aksi</th>
                                        </tr>
                                    </tfoot>
                                    <tbody>
                                        <?php if (!empty($pegawai)) : ?>
                                            <?php foreach ($pegawai as $p): ?>
                                                <tr>
                                                    <td><?= $p->id_pegawai; ?></td>
                                                    <td><?= $p->nik; ?></td>
                                                    <td><?= $p->nama; ?></td>
                                                    <td><?= $p->username; ?></td>
                                                    <td><?= $p->jenis_kelamin; ?></td>
                                                    <td><?= $p->email; ?></td>
                                                    <td><?= $p->role; ?></td>
                                                    <td><?= $p->tanggal_masuk; ?></td>
                                                    <td><?= $p->status; ?></td>
                                                    <td><?= $p->gaji; ?></td>
                                                    <td>
                                                        <?php if ($this->session->userdata('role') == 1 || $this->session->userdata('role') == 8): ?>
                                                            <a href="<?= base_url('Pegawai/editPegawai/' . $p->id_pegawai); ?>" class="btn btn-primary btn-sm">Edit</a>
                                                        <?php endif; ?>
                                                        <?php if ($this->session->userdata('role') == 8): ?>
                                                            <a href="<?= base_url('Pegawai/hapusPegawai/' . $p->id_pegawai); ?>"
                                                                class="btn btn-danger btn-sm btn-hapus">
                                                                <i class="fas fa-trash"></i> Hapus
                                                            </a>
                                                        <?php endif; ?>
                                                    </td>
                                                </tr>
                                            <?php endforeach; ?>
                                        <?php else : ?>
                                            <tr>
                                                <td colspan="11" class="text-center text-muted">
                                                    Data tidak ditemukan
                                                </td>
                                            </tr>
                                        <?php endif; ?>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>

                </div>
                <!-- /.container-fluid -->

            </div>
            <!-- End of Main Content -->
            <?php $this->load->view('footer'); ?>
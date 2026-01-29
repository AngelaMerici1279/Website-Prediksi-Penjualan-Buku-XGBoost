<?php
// $this->load->view('headerdashboard/headerKepegawaian');
// $this->load->view('sidebar');
// $this->load->view('topbar');

?>
<!-- Begin Page Content -->
<div class="container-fluid">

    <!-- Page Heading -->
    <h1 class="h3 mb-4 text-gray-800">Data Pegawai</h1>

    <div class="row">
        <div class="col-xl-3 col-md-6 mb-4">
            <div class="card border-left-primary shadow h-100 py-2 position-relative">
                <a href="<?php echo site_url('dataKepegawaian'); ?>" class="stretched-link"></a>
                <div class="card-body">
                    <div class="row no-gutters align-items-center">
                        <div class="col mr-2">
                            <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">
                                Pegawai Penjualan</div>
                            <div class="h5 mb-0 font-weight-bold text-gray-800"><?php echo $Penjualan; ?></div>
                        </div>
                        <div class="col-auto">
                            <i class="fas fa-shopping-cart fa-3x text-primary"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="col-xl-3 col-md-6 mb-4">
            <div class="card border-left-success shadow h-100 py-2">
                <div class="card-body">
                    <div class="row no-gutters align-items-center">
                        <div class="col mr-2">
                            <div class="text-xs font-weight-bold text-success text-uppercase mb-1">
                                Pegawai Kepegawaian</div>
                            <div class="h5 mb-0 font-weight-bold text-gray-800"><?php echo $Kepegawaian; ?></div>
                        </div>
                        <div class="col-auto">
                            <i class="fas fa-credit-card fa-3x text-success"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Pegawai Percetakan -->
        <div class="col-xl-3 col-md-6 mb-4">
            <div class="card border-left-warning shadow h-100 py-2">
                <div class="card-body">
                    <div class="row no-gutters align-items-center">
                        <div class="col mr-2">
                            <div class="text-xs font-weight-bold text-warning text-uppercase mb-1">
                                Pegawai Percetakan</div>
                            <div class="h5 mb-0 font-weight-bold text-gray-800"><?php echo $Percetakan; ?></div>
                        </div>
                        <div class="col-auto">
                            <i class="fas fa-print fa-3x text-warning"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Pegawai Pemasaran -->
        <div class="col-xl-3 col-md-6 mb-4">
            <div class="card border-left-info shadow h-100 py-2">
                <div class="card-body">
                    <div class="row no-gutters align-items-center">
                        <div class="col mr-2">
                            <div class="text-xs font-weight-bold text-info text-uppercase mb-1">
                                Pegawai Pemasaran</div>
                            <div class="h5 mb-0 font-weight-bold text-gray-800"><?php echo $Pemasaran; ?></div>
                        </div>
                        <div class="col-auto">
                            <i class="fas fa-bullhorn fa-3x text-info"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Pegawai SDM -->
        <div class="col-xl-3 col-md-6 mb-4">
            <div class="card border-left-danger shadow h-100 py-2">
                <div class="card-body">
                    <div class="row no-gutters align-items-center">
                        <div class="col mr-2">
                            <div class="text-xs font-weight-bold text-danger text-uppercase mb-1">
                                Pegawai Pembelian</div>
                            <div class="h5 mb-0 font-weight-bold text-gray-800"><?php echo $Pembelian; ?></div>
                        </div>
                        <div class="col-auto">
                            <i class="fas fa-users fa-3x text-danger"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Programmer -->
        <div class="col-xl-3 col-md-6 mb-4">
            <div class="card border-left-danger shadow h-100 py-2">
                <div class="card-body">
                    <div class="row no-gutters align-items-center">
                        <div class="col mr-2">
                            <div class="text-xs font-weight-bold text-danger text-uppercase mb-1">
                                Programmer</div>
                            <div class="h5 mb-0 font-weight-bold text-gray-800"><?php echo $Programmer; ?></div>
                        </div>
                        <div class="col-auto">
                            <i class="fas fa-users fa-3x text-danger"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

</div>
<!-- /.container-fluid -->

</div>
<!-- End of Main Content -->
<?php $this->load->view('footer'); ?>
<script>
    $(document).on('click', '.btn-hapus', function(e) {
        e.preventDefault(); // Mencegah link langsung terbuka
        const href = $(this).attr('href');

        Swal.fire({
            title: 'Apakah Anda yakin?',
            text: "Data pegawai ini akan dihapus secara permanen!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Ya, Hapus!',
            cancelButtonText: 'Batal'
        }).then((result) => {
            if (result.isConfirmed) {
                // Jika user klik "Ya", arahkan ke URL hapus
                document.location.href = href;
            }
        });
    });
</script>
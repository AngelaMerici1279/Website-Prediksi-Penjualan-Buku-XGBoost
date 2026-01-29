<?php $this->load->view('headerdashboard/headerKepegawaian');
$this->load->view('sidebar');
$this->load->view('topbar'); ?>

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
                    <h1 class="h3 mb-2 text-gray-800">Dashboard</h1>

                    <!-- Content Row -->
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
                        <div class="col-xl-8 col-lg-7">

                            <!-- Area Chart -->
                            <div class="card shadow mb-4">
                                <div class="card-header py-3">
                                    <h6 class="m-0 font-weight-bold text-primary">Tanggal Pegawai Masuk</h6>
                                </div>
                                <div class="card-body">
                                    <div class="chart-area">
                                        <canvas id="myAreaChart"></canvas>
                                    </div>
                                    <!-- <hr>
                                    Styling for the area chart can be found in the
                                    <code>/js/demo/chart-area-demo.js</code> file. -->
                                </div>
                            </div>

                            <!-- Bar Chart -->
                            <div class="card shadow mb-4">
                                <div class="card-header py-3">
                                    <h6 class="m-0 font-weight-bold text-primary">Jumlah Pegawai Berdasarkan Role</h6>
                                </div>
                                <div class="card-body">
                                    <div class="chart-bar">
                                        <canvas id="myBarChart"></canvas>
                                    </div>
                                    <!-- <hr>
                                    Styling for the bar chart can be found in the
                                    <code>/js/demo/chart-bar-demo.js</code> file. -->
                                </div>
                            </div>

                        </div>

                        <!-- Donut Chart -->
                        <div class="col-xl-4 col-lg-5">
                            <div class="card shadow mb-4">
                                <!-- Card Header - Dropdown -->
                                <div class="card-header py-3">
                                    <h6 class="m-0 font-weight-bold text-primary"> Chart Status Pegawai</h6>
                                </div>
                                <!-- Card Body -->
                                <div class="card-body">
                                    <div class="chart-pie pt-4">
                                        <canvas id="myPieChart"></canvas>
                                    </div>
                                    <hr>
                                </div>
                            </div>
                        </div>
                    </div>

                </div>
                <!-- /.container-fluid -->

            </div>
            <!-- End of Main Content -->

            <!-- Footer -->
            <footer class="sticky-footer bg-white">
                <div class="container my-auto">
                    <div class="copyright text-center my-auto">
                        <span>Copyright &copy; Your Website 2025</span>
                    </div>
                </div>
            </footer>
            <!-- End of Footer -->

        </div>
        <!-- End of Content Wrapper -->

    </div>
    <!-- End of Page Wrapper -->

    <!-- Bootstrap core JavaScript-->
    <script src="<?= base_url('assets/'); ?>vendor/jquery/jquery.min.js"></script>
    <script src="<?= base_url('assets/'); ?>vendor/bootstrap/js/bootstrap.bundle.min.js"></script>

    <!-- Core plugin JavaScript-->
    <script src="<?= base_url('assets/'); ?>vendor/jquery-easing/jquery.easing.min.js"></script>

    <!-- Custom scripts for all pages-->
    <script src="<?= base_url('assets/'); ?>js/sb-admin-2.min.js"></script>

    <!-- Page level plugins -->
    <script src="<?= base_url('assets/'); ?>vendor/chart.js/Chart.min.js"></script>

    <script>
        const barChartData = <?php echo json_encode($roleBar); ?>;

        const labelsBar = barChartData.map(item => 'Role ' + item.role_id); // bisa diganti nama role
        const dataBar = barChartData.map(item => item.jumlah);

        const ctx2 = document.getElementById('myBarChart').getContext('2d');
        const myBarChart = new Chart(ctx2, {
            type: 'bar',
            data: {
                labels: labelsBar,
                datasets: [{
                    label: 'Jumlah Pegawai',
                    data: dataBar,
                    backgroundColor: '#4e73df',
                    hoverBackgroundColor: '#2e59d9',
                    borderColor: '#4e73df',
                }],
            },
            options: {
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                }
            }
        });
    </script>
    <script>
        // Ambil data dari PHP
        const statusChartData = <?php echo json_encode($chartStatus); ?>;

        // Siapkan label & data
        const labels = statusChartData.map(item => item.status);
        const data = statusChartData.map(item => item.total);

        // Buat Donut Chart
        const ctx = document.getElementById('myPieChart').getContext('2d');
        const myPieChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: ['#4e73df', '#1cc88a'], // ubah sesuai kebutuhan
                    hoverBackgroundColor: ['#2e59d9', '#17a673'],
                    hoverBorderColor: "rgba(234, 236, 244, 1)",
                }],
            },
            options: {
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.label + ': ' + context.parsed;
                            }
                        }
                    }
                }
            },
        });
    </script>
    <script>
        const areaChartData = <?php echo json_encode($areaChartHireDate); ?>;

        const labelsArea = areaChartData.map(item => item.bulan);
        const dataArea = areaChartData.map(item => item.jumlah);

        const ctx3 = document.getElementById('myAreaChart').getContext('2d');
        const myAreaChart = new Chart(ctx3, {
            type: 'line', // area chart = line chart dengan fill
            data: {
                labels: labelsArea,
                datasets: [{
                    label: 'Jumlah Pegawai Baru',
                    data: dataArea,
                    fill: true, // bikin area di bawah line
                    backgroundColor: 'rgba(78, 115, 223, 0.2)',
                    borderColor: 'rgba(78, 115, 223, 1)',
                    tension: 0.3
                }],
            },
            options: {
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                },
                plugins: {
                    legend: {
                        display: true
                    }
                }
            }
        });
    </script>



    <!-- Page level custom scripts -->
    <script src="<?= base_url('assets/'); ?>js/demo/chart-area-demo.js"></script>
    <script src="<?= base_url('assets/'); ?>js/demo/chart-pie-demo.js"></script>
    <script src="<?= base_url('assets/'); ?>js/demo/chart-bar-demo.js"></script>


</body>

</html>
<div class="container">

    <!-- Outer Row -->
    <div class="row justify-content-center">

        <div class="col-lg-6" style="min-height: 100vh; padding-top: 80px;">

            <div class="card o-hidden border-0 shadow-lg my-5" style="background-color: rgba(255, 255, 255, 0.7);">
                <div class="card-body p-0">
                    <!-- Nested Row within Card Body -->
                    <div class="row">
                        <div class="col-lg">
                            <div class="p-5">
                                <div class="text-center">
                                    <h1 class="h4 text-gray-900 mb-4">Login Page</h1>
                                </div>
                                <?php if ($this->session->flashdata('error')): ?>
                                    <div style="color: red;">
                                        <?php echo $this->session->flashdata('error'); ?>
                                    </div>
                                <?php endif; ?>
                                <form class="user" method="post" action="<?php echo site_url('auth/login_process'); ?>">
                                    <div class="form-group">
                                        <input type="text" class="form-control form-control-user"
                                            id="username" name="username" aria-describedby="emailHelp"
                                            placeholder="Masukkan Username">
                                    </div>
                                    <div class="form-group">
                                        <input type="password" class="form-control form-control-user"
                                            id="password" name="password" placeholder="Masukkan Password">
                                    </div>
                                    <!-- <div class="form-group">
                                            <div class="custom-control custom-checkbox small">
                                                <input type="checkbox" class="custom-control-input" id="customCheck">
                                                <label class="custom-control-label" for="customCheck">Remember
                                                    Me</label>
                                            </div>
                                        </div> -->
                                    <button type="submit" class="btn btn-primary btn-user btn-block">
                                        Login
                                    </button>
                                    <!-- <hr> -->
                                    <!-- <a href="index.html" class="btn btn-google btn-user btn-block">
                                            <i class="fab fa-google fa-fw"></i> Login with Google
                                        </a>
                                        <a href="index.html" class="btn btn-facebook btn-user btn-block">
                                            <i class="fab fa-facebook-f fa-fw"></i> Login with Facebook
                                        </a> -->
                                </form>
                                <!-- <hr>
                                    <div class="text-center">
                                        <a class="small" href="forgot-password.html">Forgot Password?</a>
                                    </div>
                                    <div class="text-center">
                                        <a class="small" href="register.html">Create an Account!</a>
                                    </div> -->
                            </div>
                        </div>
                    </div>
                </div>
            </div>

        </div>

    </div>

</div>
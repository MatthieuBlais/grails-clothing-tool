<!DOCTYPE html>
<html lang="en">
  <head>
  <meta name='layout' content='login' />
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
    <title>MeOw</title>
  </head>
  <body>
    <form class="form-signin" id="user-login"  action="${postUrl}" method="POST" name="loginForm" novalidate="">
      <div class="text-center mb-4">
        <img class="mb-4" src="/assets/avatar_placeholder.svg" alt="" width="200" height="200">
              
      </div>

      <div class="form-label-group">
        <input type="email" name="username" class="form-control" placeholder="Email address" required="" autofocus="">
        <label for="inputEmail">Email address</label>
      </div>

      <div class="form-label-group">
        <input type="password" name="password" class="form-control" placeholder="Password" required="">
        <label for="inputPassword">Password</label>
      </div>

      <div class="checkbox mb-3">
        <label>
          <input type="checkbox" value="remember-me"> Remember me
        </label>
      </div>
      <button class="btn btn-lg btn-primary btn-block" type="submit">Sign in</button>
    </form>
  </body>
</html>



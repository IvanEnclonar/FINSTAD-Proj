
    data {
      int<lower=0> N;
      array[N] int<lower=0,upper=1> y;
      vector[N] pct_female;
      vector[N] year_std;
      vector[N] rank_numeric;
    }
    parameters {
      real alpha;
      real beta_female;
      real beta_year;
      real beta_rank;
    }
    model {
      alpha ~ normal(0, 5);
      beta_female ~ normal(0, 2);
      beta_year ~ normal(0, 2);
      beta_rank ~ normal(0, 2);
      y ~ bernoulli_logit(alpha + beta_female * pct_female + beta_year * year_std + beta_rank * rank_numeric);
    }
    
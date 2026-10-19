SELECT COUNT (*) AS total_matches
FROM matches;

SELECT COUNT (*) AS total_teams
FROM teams;

SELECT 
    m.match_id,
    m.match_date,
    home.team_name AS home_team,
    away.team_name AS away_team,
    m.home_score,
    m.away_score,
    m.full_time_result
FROM matches AS m
JOIN teams AS home
    ON m.home_team_id = home.team_id
JOIN teams AS away
    ON m.away_team_id = away.team_id
ORDER BY m.match_date, m.match_id;

SELECT
    t.team_name,
    SUM(team_stats.goals) AS total_goals
FROM (
    SELECT home_team_id AS team_id, home_score AS goals
    FROM matches

    UNION ALL

    SELECT away_team_id AS team_id, away_score AS goals
    FROM matches
) AS team_stats
JOIN teams AS t
    ON t.team_id = team_stats.team_id
GROUP BY t.team_id, t.team_name
ORDER BY total_goals DESC;

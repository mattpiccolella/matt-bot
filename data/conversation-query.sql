/* Script to query the conversations I've had on iMessage. */

SELECT
    m.rowid as message_id,
    (SELECT chat_id FROM chat_message_join WHERE chat_message_join.message_id = m.rowid) as message_group,
    DATETIME(date +978307200, 'unixepoch', 'localtime') AS date,
    CASE is_from_me
        WHEN 0 THEN "Received"
        WHEN 1 THEN "Sent"
        ELSE is_from_me
    END AS type,
    id AS address,
    text
FROM message AS m
LEFT JOIN handle AS h ON h.rowid = m.handle_id
LEFT JOIN (SELECT count(*) as participant_count, cmj.chat_id, cmj.message_id as mid FROM 
    chat_handle_join as chj
    INNER JOIN chat_message_join as cmj on cmj.chat_id = chj.chat_id
    GROUP BY cmj.message_id, cmj.chat_id) as p on p.mid = m.rowid
/* Only select individual messages to make the messages more real. */
WHERE p.participant_count = 1
ORDER BY message_group, message_id;
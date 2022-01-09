CREATE TABLE Inventory (
    ID TEXT PRIMARY KEY,
    Quantity INTEGER NOT NULL,
    Description TEXT,
    DateAdded TEXT
);

CREATE VIRTUAL TABLE InventoryFTS
USING fts5(
    content='Inventory',
    content_rowid='rowid',
    ID UNINDEXED,
    Quantity UNINDEXED,
    Description,
    DateAdded UNINDEXED
);

CREATE TRIGGER InventoryFTS_ai AFTER INSERT ON Inventory BEGIN
  INSERT INTO InventoryFTS(rowid, Description) VALUES (new.rowid, new.Description);
END;
CREATE TRIGGER InventoryFTS_ad AFTER DELETE ON Inventory BEGIN
  INSERT INTO InventoryFTS(InventoryFTS, rowid, Description) VALUES('delete', old.rowid, old.Description);
END;
CREATE TRIGGER InventoryFTS_au AFTER UPDATE ON Inventory BEGIN
  INSERT INTO InventoryFTS(InventoryFTS, rowid, Description) VALUES('delete', old.rowid, old.Description);
  INSERT INTO InventoryFTS(rowid, Description) VALUES (new.rowid, new.Description);
END;
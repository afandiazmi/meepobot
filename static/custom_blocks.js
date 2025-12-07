// Register custom blocks for MEEPOBOT movement
function defineRobotBlocks() {
  // --- Block 1: Move Direction for Duration ---
Blockly.Blocks['robot_move'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Move")
        .appendField(new Blockly.FieldDropdown([
            ["Forward", "forward"], 
            ["Backward", "backward"], 
            ["Left", "left"], 
            ["Right", "right"]
        ]), "DIRECTION");
    this.appendValueInput("DURATION")
        .setCheck("Number")
        .appendField("for");
    this.appendDummyInput()
        .appendField("seconds");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(160);
    this.setTooltip("Move the robot in a specified direction for a set duration.");
    this.setHelpUrl("");
  }
};

// Defines the JavaScript code generator for 'robot_move'
Blockly.JavaScript['robot_move'] = function(block) {
  const direction = block.getFieldValue('DIRECTION');
  const duration = Blockly.JavaScript.valueToCode(block, 'DURATION', Blockly.JavaScript.ORDER_ATOMIC) || '0';
  
  // The output format is a string command that your backend Python script (or equivalent) expects,
  // typically 'command:duration'. Example: 'forward:3'
  const code = `'${direction}:${duration}'`; 
  return code + ';\n';
};

// Defines the 'robot_stop' block
Blockly.Blocks['robot_stop'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("STOP");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(160);
    this.setTooltip("Stop all robot movement immediately.");
    this.setHelpUrl("");
  }
};

// Defines the JavaScript code generator for 'robot_stop'
Blockly.JavaScript['robot_stop'] = function(block) {
  // Output a simple 'stop' command
  const code = "'stop:0'";
  return code + ';\n';
};

// Register generators (how Blockly turns the blocks into text)
function registerRobotGenerators(generator) {
  // Generator for the Move block
  generator["robot_move"] = function (block) {
    const direction = block.getFieldValue("DIRECTION");
    const duration =
      generator.valueToCode(block, "DURATION", generator.ORDER_NONE) || "1";
    // Generate the instruction string: e.g., "t_up:2"
    const code = `${direction}:${duration}`;
    return code;
  };

  // Generator for the Stop block
  generator["robot_stop"] = function (block) {
    // We'll use a short stop duration to separate commands
    const code = "t_stop:0.1";
    return code;
  };
}

// Call the functions to define and register the blocks
defineRobotBlocks();
registerRobotGenerators(Blockly.JavaScript);
